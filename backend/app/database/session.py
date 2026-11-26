from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import Session, sessionmaker, with_loader_criteria

from app.core.config import settings
from app.database.base import ProjectScopedMixin


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@event.listens_for(Session, "do_orm_execute")
def apply_active_project_scope(execute_state) -> None:
    project_id = execute_state.session.info.get("project_id")
    if project_id is None:
        return

    if (
        execute_state.is_select
        or execute_state.is_update
        or execute_state.is_delete
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                ProjectScopedMixin,
                lambda model: model.project_id == project_id,
                include_aliases=True,
            )
        )


@event.listens_for(Session, "before_flush")
def enforce_project_on_writes(session, flush_context, instances) -> None:
    project_id = session.info.get("project_id")
    if project_id is None:
        return

    for instance in session.new.union(session.dirty).union(session.deleted):
        if not isinstance(instance, ProjectScopedMixin):
            continue
        if instance.project_id is None:
            instance.project_id = project_id
        elif instance.project_id != project_id:
            raise ValueError("A request cannot write to another project.")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()