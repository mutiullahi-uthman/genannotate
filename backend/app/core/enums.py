# app/core/enums.py

from enum import Enum


class StrEnum(str, Enum):
    """
    Base enum for consistent string behaviour.
    """

    def __str__(self) -> str:
        return self.value


# ==========================================================
# USER & AUTH
# ==========================================================

class UserRole(StrEnum):
    ADMIN = "ADMIN"
    ANNOTATOR = "ANNOTATOR"
    SUPERVISOR = "SUPERVISOR"
    RESEARCH_LEAD = "RESEARCH_LEAD"


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Permission(StrEnum):
    DATASET_CREATE = "DATASET_CREATE"
    DATASET_DELETE = "DATASET_DELETE"
    USER_MANAGE = "USER_MANAGE"
    CODEBOOK_MANAGE = "CODEBOOK_MANAGE"
    RECORD_ASSIGN = "RECORD_ASSIGN"
    REVIEW_APPROVE = "REVIEW_APPROVE"
    EXPORT_GENERATE = "EXPORT_GENERATE"


# ==========================================================
# DATASETS
# ==========================================================

class DatasetStatus(StrEnum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class DatasetSourceType(StrEnum):
    CSV = "CSV"
    XLSX = "XLSX"
    JSON = "JSON"


# ==========================================================
# IMPORTS
# ==========================================================

class ImportStatus(StrEnum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    IMPORTING = "IMPORTING"
    IMPORTED = "IMPORTED"
    FAILED = "FAILED"


class ValidationStatus(StrEnum):
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"


# ==========================================================
# RECORD WORKFLOW
# ==========================================================

class RecordState(StrEnum):
    IMPORTED = "IMPORTED"

    UNASSIGNED = "UNASSIGNED"

    ASSIGNED = "ASSIGNED"

    IN_PROGRESS = "IN_PROGRESS"

    SUBMITTED = "SUBMITTED"

    FLAGGED = "FLAGGED"

    SUPERVISOR_REVIEW = "SUPERVISOR_REVIEW"

    RETURNED = "RETURNED"

    APPROVED = "APPROVED"

    EXPORTED = "EXPORTED"


# ==========================================================
# ASSIGNMENTS
# ==========================================================

class AssignmentType(StrEnum):
    MANUAL = "MANUAL"
    BULK = "BULK"
    REASSIGNMENT = "REASSIGNMENT"


# ==========================================================
# ANNOTATION
# ==========================================================

class AnnotationStatus(StrEnum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    RETURNED = "RETURNED"
    APPROVED = "APPROVED"


# ==========================================================
# FREQUENCY
# MVP DEFAULT VALUES
# Instrument specific mappings can come later
# ==========================================================

class FrequencyCategory(StrEnum):
    DAILY = "DAILY"
    SEVERAL_DAYS = "SEVERAL_DAYS"
    MORE_THAN_HALF_THE_DAYS = "MORE_THAN_HALF_THE_DAYS"
    NEARLY_EVERY_DAY = "NEARLY_EVERY_DAY"

    NOT_STATED = "NOT_STATED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


# ==========================================================
# CULTURAL FLAGS
# ==========================================================

class CulturalFlag(StrEnum):
    NONE = "NONE"
    PRESENT = "PRESENT"
    NEEDS_REVIEW = "NEEDS_REVIEW"


# ==========================================================
# RISK
# ==========================================================

class RiskLevel(StrEnum):
    NONE = "NONE"

    NEEDS_REVIEW = "NEEDS_REVIEW"

    HIGH = "HIGH"


class RiskStatus(StrEnum):
    OPEN = "OPEN"
    IN_REVIEW = "IN_REVIEW"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# ==========================================================
# REVIEW
# ==========================================================

class ReviewDecision(StrEnum):
    APPROVE = "APPROVE"

    RETURN = "RETURN"

    DISAGREEMENT = "DISAGREEMENT"

    REOPEN = "REOPEN"


class ReviewStatus(StrEnum):
    PENDING = "PENDING"

    IN_REVIEW = "IN_REVIEW"

    APPROVED = "APPROVED"

    RETURNED = "RETURNED"

    RESOLVED = "RESOLVED"


# ==========================================================
# FLAGS
# ==========================================================

class FlagType(StrEnum):
    RISK = "RISK"
    QUALITY = "QUALITY"
    CULTURAL = "CULTURAL"
    UNCLEAR_TRANSCRIPT = "UNCLEAR_TRANSCRIPT"
    OTHER = "OTHER"


class FlagStatus(StrEnum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"


# ==========================================================
# CODEBOOK
# ==========================================================

class CodebookStatus(StrEnum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


# ==========================================================
# EXPORTS
# ==========================================================

class ExportFormat(StrEnum):
    CSV = "CSV"
    JSON = "JSON"


class ExportStatus(StrEnum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ==========================================================
# FILE STORAGE
# ==========================================================

class FileType(StrEnum):
    DATASET = "DATASET"
    EXPORT = "EXPORT"
    CODEBOOK = "CODEBOOK"
    AUDIT_ARCHIVE = "AUDIT_ARCHIVE"


# ==========================================================
# AUDIT TRAIL
# ==========================================================

class AuditAction(StrEnum):
    CREATE = "CREATE"

    UPDATE = "UPDATE"

    DELETE = "DELETE"

    ASSIGN = "ASSIGN"

    REASSIGN = "REASSIGN"

    SAVE_DRAFT = "SAVE_DRAFT"

    SUBMIT = "SUBMIT"

    FLAG = "FLAG"

    APPROVE = "APPROVE"

    RETURN = "RETURN"

    REOPEN = "REOPEN"

    EXPORT = "EXPORT"

    LOGIN = "LOGIN"

    LOGOUT = "LOGOUT"


class AuditEntity(StrEnum):
    USER = "USER"

    DATASET = "DATASET"

    RECORD = "RECORD"

    ANNOTATION = "ANNOTATION"

    REVIEW = "REVIEW"

    EXPORT = "EXPORT"

    CODEBOOK = "CODEBOOK"

    ASSIGNMENT = "ASSIGNMENT"

    FILE = "FILE"


# ==========================================================
# SYSTEM JOBS
# ==========================================================

class JobStatus(StrEnum):
    PENDING = "PENDING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


# ==========================================================
# SUPPORTED LANGUAGES
# PROJECT CONFIGURABLE
# MVP DEFAULTS FROM SPEC
# ==========================================================

class SupportedLanguage(StrEnum):
    ENGLISH = "ENGLISH"

    NIGERIAN_PIDGIN = "NIGERIAN_PIDGIN"

    YORUBA = "YORUBA"

    HAUSA = "HAUSA"

    IGBO = "IGBO"
    
    
# ==========================================================
# IMPORT JOBS
# ==========================================================  

class ImportJobStatus(StrEnum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    VALIDATING = "VALIDATING"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    VALIDATED = "VALIDATED"
    IMPORTING = "IMPORTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"  
    
# ==========================================================
# ASSIGNMENT TYPES
# ========================================================== 

class AssignmentType(StrEnum):
    MANUAL = "MANUAL"
    BULK = "BULK"
    REASSIGNMENT = "REASSIGNMENT"    
    