import asyncio
from uuid import uuid4
import random
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.sql import text
from passlib.context import CryptContext
from app.models import (
    Role,
    EmploymentType,
    User,
    Specialist,
    Vacancy,
    SpecialistSkill,
    SpecialistExperience,
    Application,
    AnalysisResult,
)
from core.config import config
from core.elasticsearch import es_client

DATABASE_URL = config.POSTGRES_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def clear_database(db: AsyncSession):
    await db.execute(text("TRUNCATE TABLE analysis_results CASCADE"))
    await db.execute(text("TRUNCATE TABLE applications CASCADE"))
    await db.execute(text("TRUNCATE TABLE specialist_experience CASCADE"))
    await db.execute(text("TRUNCATE TABLE specialist_skills CASCADE"))
    await db.execute(text("TRUNCATE TABLE specialists CASCADE"))
    await db.execute(text("TRUNCATE TABLE vacancies CASCADE"))
    await db.execute(text("TRUNCATE TABLE users CASCADE"))
    await db.execute(text("TRUNCATE TABLE roles CASCADE"))
    await db.execute(text("TRUNCATE TABLE employment_types CASCADE"))
    await db.commit()


async def generate_roles(db: AsyncSession, role_names: list = ["hr", "user"]):
    roles = []
    for name in role_names:
        role = Role(name=name)
        db.add(role)
        roles.append(role)
    await db.commit()
    return roles


async def generate_employment_types(db: AsyncSession, type_names: list = ["full-time", "part-time"]):
    employment_types = []
    for name in type_names:
        emp_type = EmploymentType(name=name)
        db.add(emp_type)
        employment_types.append(emp_type)
    await db.commit()
    return employment_types


async def generate_superuser(db: AsyncSession, email: str, username: str, full_name: str, password: str):
    admin_role = await db.execute(text("SELECT * FROM roles WHERE name = 'admin'"))
    admin_role = admin_role.mappings().first()

    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        await db.commit()
        await db.refresh(admin_role)

    existing_user = await db.execute(
        text("SELECT * FROM users WHERE email = :email OR username = :username"), {"email": email, "username": username}
    )
    if existing_user.mappings().first():
        raise ValueError(f"User with email {email} or username {username} already exists.")

    superuser = User(
        uuid=uuid4(),
        email=email,
        password=pwd_context.hash(password),
        username=username,
        full_name=full_name,
        is_active=True,
        role_id=admin_role.o_id,
    )
    db.add(superuser)
    await db.commit()
    return superuser


async def generate_users(db: AsyncSession, roles: list, hr_count: int = 2, user_count: int = 3):
    hr_role = next(role for role in roles if role.name == "hr")
    user_role = next(role for role in roles if role.name == "user")

    users = []

    for _ in range(hr_count):
        user = User(
            uuid=uuid4(),
            email=fake.unique.email(),
            password=pwd_context.hash("123123qwe"),
            username=fake.unique.user_name(),
            full_name=fake.name(),
            is_active=True,
            role_id=hr_role.o_id,
        )
        db.add(user)
        users.append(user)

    for _ in range(user_count):
        user = User(
            uuid=uuid4(),
            email=fake.unique.email(),
            password=pwd_context.hash("123123qwe"),
            username=fake.unique.user_name(),
            full_name=fake.name(),
            is_active=True,
            role_id=user_role.o_id,
        )
        db.add(user)
        users.append(user)

    await db.commit()
    return users


async def generate_specialists(db: AsyncSession, users: list, employment_types: list, count: int = 50):
    user_role_users = [user for user in users if user.role.name == "user"]
    if not user_role_users:
        raise ValueError("No users with role 'user' found to create specialists.")

    specialists = []
    for _ in range(count):
        specialist = Specialist(
            uuid=uuid4(),
            created_by=random.choice(user_role_users).o_id,
            full_name=fake.name(),
            about_me=fake.text(max_nb_chars=200),
            position=fake.job(),
            employment_type_id=random.choice(employment_types).o_id,
        )
        db.add(specialist)
        specialists.append(specialist)
    await db.commit()
    return specialists


async def generate_vacancies(db: AsyncSession, users: list, employment_types: list, count: int = 50):
    hr_role_users = [user for user in users if user.role.name == "hr"]
    if not hr_role_users:
        raise ValueError("No users with role 'hr' found to create vacancies.")

    vacancies = []
    for _ in range(count):
        vacancy = Vacancy(
            uuid=uuid4(),
            title=fake.job(),
            description=fake.text(max_nb_chars=500),
            requirements=fake.text(max_nb_chars=300),
            conditions=fake.text(max_nb_chars=300),
            salary=random.randint(10000, 150000),
            employment_type_id=random.choice(employment_types).o_id,
            created_by=random.choice(hr_role_users).o_id,
        )
        db.add(vacancy)
        vacancies.append(vacancy)
    await db.commit()
    return vacancies


async def generate_specialist_skills(db: AsyncSession, specialists: list, count_per_specialist: int = 4):
    skills = [
        "Python",
        "JavaScript",
        "TypeScript",
        "Java",
        "C#",
        "C++",
        "Go",
        "Rust",
        "Ruby",
        "PHP",
        "Kotlin",
        "Swift",
        "Dart",
        "R",
        "Scala",
        "Perl",
        "Haskell",
        "Lua",
        "Elixir",
        "Clojure",
        "React",
        "Angular",
        "Vue.js",
        "Node.js",
        "Express.js",
        "FastAPI",
        "Django",
        "Flask",
        "Spring Boot",
        "Ruby on Rails",
        "Laravel",
        ".NET Core",
        "ASP.NET",
        "TensorFlow",
        "PyTorch",
        "jQuery",
        "Bootstrap",
        "Svelte",
        "Next.js",
        "Nuxt.js",
        "SQL",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "SQLite",
        "Oracle",
        "MariaDB",
        "Cassandra",
        "DynamoDB",
        "Elasticsearch",
        "Neo4j",
        "CouchDB",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "Google Cloud Platform",
        "Terraform",
        "Ansible",
        "Jenkins",
        "GitLab CI/CD",
        "GitHub Actions",
        "CircleCI",
        "Prometheus",
        "Grafana",
        "Nginx",
        "Apache",
        "Helm",
        "Puppet",
        "Chef",
        "Vault",
        "Git",
        "Linux",
        "Bash",
        "PowerShell",
        "REST API",
        "GraphQL",
        "gRPC",
        "WebSocket",
        "Webpack",
        "Vite",
        "Postman",
        "Jira",
        "Confluence",
        "Trello",
        "Figma",
        "Sketch",
        "Pandas",
        "NumPy",
        "SciPy",
        "Scikit-learn",
        "Keras",
        "XGBoost",
        "LightGBM",
        "CatBoost",
        "Tableau",
        "Power BI",
        "Matplotlib",
        "Seaborn",
        "Apache Spark",
        "Hadoop",
        "Selenium",
        "Cypress",
        "Jest",
        "Mocha",
        "Chai",
        "Pytest",
        "JUnit",
        "TestNG",
        "Postman",
        "SoapUI",
        "LoadRunner",
        "Agile",
        "Scrum",
        "Kanban",
        "UI/UX Design",
        "Cybersecurity",
        "Blockchain",
        "Web3",
        "IoT",
        "AR/VR Development",
        "Game Development",
        "Unreal Engine",
        "Unity",
    ]
    for specialist in specialists:
        for _ in range(count_per_specialist):
            skill = SpecialistSkill(
                specialist_id=specialist.o_id,
                skill_name=random.choice(skills),
            )
            db.add(skill)
    await db.commit()


async def generate_specialist_experiences(db: AsyncSession, specialists: list, count_per_specialist: int = 5):
    for specialist in specialists:
        for _ in range(count_per_specialist):
            start_date = fake.date_between(start_date="-10y", end_date="-1y")
            end_date = fake.date_between(start_date=start_date, end_date="today")
            experience = SpecialistExperience(
                uuid=uuid4(),
                specialist_id=specialist.o_id,
                company_name=fake.company(),
                position=fake.job(),
                start_date=start_date,
                end_date=end_date,
            )
            db.add(experience)
    await db.commit()


async def generate_applications(db: AsyncSession, specialists: list, vacancies: list, count: int = 30):
    existing_pairs = set()
    attempts = 0
    max_attempts = count * 2
    while len(existing_pairs) < count and attempts < max_attempts:
        specialist = random.choice(specialists)
        vacancy = random.choice(vacancies)
        pair = (specialist.uuid, vacancy.uuid)
        if pair not in existing_pairs:
            application = Application(
                specialist_uuid=specialist.uuid,
                vacancy_uuid=vacancy.uuid,
                applied=random.choice([True, False]),
            )
            db.add(application)
            existing_pairs.add(pair)
        attempts += 1
    await db.commit()


async def generate_analysis_results(db: AsyncSession, specialists: list, vacancies: list, count: int = 25):
    for _ in range(count):
        result = AnalysisResult(
            vacancy_uuid=random.choice(vacancies).uuid,
            specialist_uuid=random.choice(specialists).uuid,
            match_percentage=round(random.uniform(50.00, 99.99), 2),
            mismatches=[fake.sentence() for _ in range(random.randint(0, 3))] if random.choice([True, False]) else None,
        )
        db.add(result)
    await db.commit()


async def main():
    fake.unique.clear()
    async with AsyncSessionLocal() as db:
        await clear_database(db)

        roles = await generate_roles(db, role_names=["hr", "user"])
        employment_types = await generate_employment_types(db, type_names=["full-time", "part-time"])

        users = await generate_users(db, roles, hr_count=50, user_count=120)
        specialists = await generate_specialists(db, users, employment_types, count=120)
        vacancies = await generate_vacancies(db, users, employment_types, count=50)
        await generate_specialist_skills(db, specialists, count_per_specialist=10)
        await generate_specialist_experiences(db, specialists, count_per_specialist=4)
        await generate_applications(db, specialists, vacancies, count=35)
        await generate_analysis_results(db, specialists, vacancies, count=35)
        await generate_superuser(
            db=db,
            email="email@example.com",
            username="actusnileh",
            full_name="Actus Nileh",
            password="123123qwe",
        )

        for vacancy in vacancies:
            document = {
                "o_id": vacancy.o_id,
                "uuid": str(vacancy.uuid),
                "title": vacancy.title,
                "description": vacancy.description,
                "requirements": vacancy.requirements,
                "conditions": vacancy.conditions,
                "salary": vacancy.salary,
                "employment_type_id": vacancy.employment_type_id,
            }
            await es_client.index(index="vacancies", id=vacancy.o_id, document=document)


if __name__ == "__main__":
    asyncio.run(main())
