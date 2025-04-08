from typing import Dict, Any, List

from .Conversations import ConversationManager
from .Comments import CommentManager
from .Users import UserManager
from .Vote import VoteManager
from .Report import ReportManager
from .MigrationRecord import MigrationRecordManager
from .utils import create_db_and_tables


class DatabaseActor(
    UserManager, 
    ConversationManager, 
    CommentManager, 
    VoteManager, 
    ReportManager,
    MigrationRecordManager
):
    """
    DatabaseActor class for LitePolis.

    This class serves as the central point of interaction between the LitePolis system
    and the database module. It aggregates operations from various manager classes,
    such as UserManager, ConversationManager, CommentManager, VoteManager, and ReportManager,
    providing a unified interface for database interactions.
    """
    pass

create_db_and_tables()