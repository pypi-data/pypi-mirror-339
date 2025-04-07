"""Command implementation for parsing codebases."""
from pathlib import Path

from knowlang.cli.display.formatters import get_formatter
from knowlang.cli.types import ParseCommandArgs
from knowlang.cli.utils import create_config
from knowlang.indexing.codebase_manager import CodebaseManager
from knowlang.indexing.increment_update import IncrementalUpdater
from knowlang.indexing.indexing_agent import IndexingAgent
from knowlang.indexing.state_manager import StateManager
from knowlang.indexing.state_store.base import StateChangeType
from knowlang.parser.factory import CodeParserFactory
from knowlang.utils import FancyLogger

LOG = FancyLogger(__name__)


async def parse_command(args: ParseCommandArgs) -> None:
    """Execute the parse command.
    
    Args:
        args: Typed command line arguments
    """
    # Load configuration
    config = create_config(args.config)
    
    # Update codebase directory in config
    config.db.codebase_directory = Path(args.path).resolve()
    config.db.codebase_url = args.path
    config.user_id = args.user_id
    
    # Create parser code_parser_factory
    code_parser_factory = CodeParserFactory(config)
    codebase_manager = CodebaseManager(config)
    state_manager = StateManager(config)
    
    # Process files
    total_chunks = []
    
    codebase_files = await codebase_manager.get_current_files()
    LOG.info(f"Found {len(codebase_files)} files in codebase directory")
    file_changes = await state_manager.state_store.detect_changes(codebase_files)
    LOG.info(f"Detected {len(file_changes)} file changes")

    for changed_file_path in [
        (config.db.codebase_directory / change.path) 
        for change in file_changes
        if change.change_type != StateChangeType.DELETED
    ]:
        
        parser = code_parser_factory.get_parser(changed_file_path)
        if parser:
            chunks = parser.parse_file(changed_file_path)
            total_chunks.extend(chunks)

    updater = IncrementalUpdater(config)
    await updater.update_codebase(
        chunks=total_chunks, 
        file_changes=file_changes
    )

    # Display results
    if total_chunks:
        LOG.info(f"\nFound {len(total_chunks)} code chunks")
        formatter = get_formatter(args.output)
        formatter.display_chunks(total_chunks)
    else:
        LOG.warning("No code chunks found")
    
    # Process summaries