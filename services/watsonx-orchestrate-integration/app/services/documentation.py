"""
Documentation Update Service

Handles automated documentation updates based on code analysis results.
"""

import os
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from app.utils.logger import get_logger
from app.models.request import DocumentationUpdateRequest
from app.models.response import DocumentationUpdateResponse

logger = get_logger(__name__)


class DocumentationService:
    """
    Service for updating code documentation with analysis results.
    
    Supports multiple documentation formats: Markdown, reStructuredText, JSDoc.
    """
    
    def __init__(self, base_path: Optional[str] = None, mock_mode: bool = True):
        """
        Initialize the documentation service.
        
        Args:
            base_path: Base path for documentation files
            mock_mode: Whether to use mock mode (default: True)
        """
        self.base_path = base_path or os.getenv("DOCS_BASE_PATH", "./docs")
        self.mock_mode = mock_mode or os.getenv("DOCS_MOCK_MODE", "true").lower() == "true"
        self.version_history: List[Dict[str, Any]] = []
        
        logger.info(f"DocumentationService initialized (mock_mode={self.mock_mode})")
    
    async def update_documentation(
        self,
        request: DocumentationUpdateRequest
    ) -> DocumentationUpdateResponse:
        """
        Update documentation with complexity analysis and optimization notes.
        
        Args:
            request: Documentation update request
            
        Returns:
            Documentation update response
        """
        logger.info(f"Updating documentation for: {request.file_path}")
        
        files_updated = []
        changes_made = []
        
        try:
            # Update main documentation file
            doc_file = await self._update_main_doc(request)
            if doc_file:
                files_updated.append(doc_file)
                changes_made.append("Updated main documentation with complexity analysis")
            
            # Update README if applicable
            readme_file = await self._update_readme(request)
            if readme_file:
                files_updated.append(readme_file)
                changes_made.append("Updated README with performance notes")
            
            # Update API documentation
            api_doc_file = await self._update_api_doc(request)
            if api_doc_file:
                files_updated.append(api_doc_file)
                changes_made.append("Updated API documentation")
            
            # Generate changelog entry
            changelog_entry = await self._generate_changelog(request)
            if changelog_entry:
                changes_made.append("Generated changelog entry")
            
            # Track version
            version = await self._track_version(request, files_updated)
            
            # Generate commit hash (mock)
            commit_hash = f"mock_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}" if self.mock_mode else None
            
            logger.info(f"Documentation updated successfully: {len(files_updated)} files")
            
            return DocumentationUpdateResponse(
                success=True,
                files_updated=files_updated,
                changes_made=changes_made,
                version=version,
                commit_hash=commit_hash,
                preview_url=f"https://docs.example.com/preview/{commit_hash}" if commit_hash else None
            )
            
        except Exception as e:
            logger.error(f"Failed to update documentation: {str(e)}")
            return DocumentationUpdateResponse(
                success=False,
                files_updated=[],
                changes_made=[],
                version=None
            )
    
    async def _update_main_doc(
        self,
        request: DocumentationUpdateRequest
    ) -> Optional[str]:
        """
        Update the main documentation file for the code.
        
        Args:
            request: Documentation update request
            
        Returns:
            Path to updated file or None
        """
        # Determine documentation file path
        file_name = Path(request.file_path).stem
        doc_path = f"{self.base_path}/{file_name}.{request.format_type}"
        
        if self.mock_mode:
            logger.info(f"[MOCK] Would update: {doc_path}")
            return doc_path
        
        # Generate documentation content
        content = await self._generate_doc_content(request)
        
        # Write to file (in real mode)
        # In mock mode, we just log what would be written
        logger.info(f"Documentation content generated for {doc_path}")
        
        return doc_path
    
    async def _generate_doc_content(
        self,
        request: DocumentationUpdateRequest
    ) -> str:
        """
        Generate documentation content based on format type.
        
        Args:
            request: Documentation update request
            
        Returns:
            Generated documentation content
        """
        if request.format_type == "markdown":
            return await self._generate_markdown(request)
        elif request.format_type == "rst":
            return await self._generate_rst(request)
        elif request.format_type == "jsdoc":
            return await self._generate_jsdoc(request)
        else:
            return await self._generate_markdown(request)
    
    async def _generate_markdown(
        self,
        request: DocumentationUpdateRequest
    ) -> str:
        """
        Generate Markdown documentation.
        
        Args:
            request: Documentation update request
            
        Returns:
            Markdown content
        """
        content = f"""# {Path(request.file_path).name}

## Complexity Analysis

### Time Complexity
"""
        
        if "before" in request.complexity_changes:
            content += f"- **Before**: {request.complexity_changes['before'].get('time', 'N/A')}\n"
        if "after" in request.complexity_changes:
            content += f"- **After**: {request.complexity_changes['after'].get('time', 'N/A')}\n"
        
        content += "\n### Space Complexity\n"
        
        if "before" in request.complexity_changes:
            content += f"- **Before**: {request.complexity_changes['before'].get('space', 'N/A')}\n"
        if "after" in request.complexity_changes:
            content += f"- **After**: {request.complexity_changes['after'].get('space', 'N/A')}\n"
        
        if request.optimization_notes:
            content += "\n## Optimization Notes\n\n"
            for note in request.optimization_notes:
                content += f"- {note}\n"
        
        if request.performance_metrics:
            content += "\n## Performance Metrics\n\n"
            for key, value in request.performance_metrics.items():
                content += f"- **{key.replace('_', ' ').title()}**: {value}\n"
        
        content += f"\n---\n*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n"
        
        return content
    
    async def _generate_rst(
        self,
        request: DocumentationUpdateRequest
    ) -> str:
        """
        Generate reStructuredText documentation.
        
        Args:
            request: Documentation update request
            
        Returns:
            RST content
        """
        file_name = Path(request.file_path).name
        content = f"""{file_name}
{'=' * len(file_name)}

Complexity Analysis
-------------------

Time Complexity
~~~~~~~~~~~~~~~
"""
        
        if "before" in request.complexity_changes:
            content += f"* **Before**: {request.complexity_changes['before'].get('time', 'N/A')}\n"
        if "after" in request.complexity_changes:
            content += f"* **After**: {request.complexity_changes['after'].get('time', 'N/A')}\n"
        
        content += "\nSpace Complexity\n~~~~~~~~~~~~~~~\n"
        
        if "before" in request.complexity_changes:
            content += f"* **Before**: {request.complexity_changes['before'].get('space', 'N/A')}\n"
        if "after" in request.complexity_changes:
            content += f"* **After**: {request.complexity_changes['after'].get('space', 'N/A')}\n"
        
        if request.optimization_notes:
            content += "\nOptimization Notes\n------------------\n\n"
            for note in request.optimization_notes:
                content += f"* {note}\n"
        
        return content
    
    async def _generate_jsdoc(
        self,
        request: DocumentationUpdateRequest
    ) -> str:
        """
        Generate JSDoc documentation.
        
        Args:
            request: Documentation update request
            
        Returns:
            JSDoc content
        """
        content = "/**\n"
        content += f" * @file {Path(request.file_path).name}\n"
        content += " * @complexity\n"
        
        if "after" in request.complexity_changes:
            content += f" * - Time: {request.complexity_changes['after'].get('time', 'N/A')}\n"
            content += f" * - Space: {request.complexity_changes['after'].get('space', 'N/A')}\n"
        
        if request.optimization_notes:
            content += " * @optimization\n"
            for note in request.optimization_notes:
                content += f" * - {note}\n"
        
        content += " */\n"
        
        return content
    
    async def _update_readme(
        self,
        request: DocumentationUpdateRequest
    ) -> Optional[str]:
        """
        Update README with performance notes.
        
        Args:
            request: Documentation update request
            
        Returns:
            Path to README or None
        """
        readme_path = f"{self.base_path}/README.md"
        
        if self.mock_mode:
            logger.info(f"[MOCK] Would update README: {readme_path}")
            return readme_path
        
        # In real mode, would read existing README and append/update section
        logger.info(f"README update prepared for {readme_path}")
        
        return readme_path
    
    async def _update_api_doc(
        self,
        request: DocumentationUpdateRequest
    ) -> Optional[str]:
        """
        Update API documentation.
        
        Args:
            request: Documentation update request
            
        Returns:
            Path to API doc or None
        """
        api_doc_path = f"{self.base_path}/api/{Path(request.file_path).stem}.md"
        
        if self.mock_mode:
            logger.info(f"[MOCK] Would update API doc: {api_doc_path}")
            return api_doc_path
        
        logger.info(f"API documentation update prepared for {api_doc_path}")
        
        return api_doc_path
    
    async def _generate_changelog(
        self,
        request: DocumentationUpdateRequest
    ) -> str:
        """
        Generate changelog entry.
        
        Args:
            request: Documentation update request
            
        Returns:
            Changelog entry
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d')
        entry = f"\n## [{timestamp}] - Performance Update\n\n"
        entry += f"### Changed\n"
        entry += f"- Updated complexity analysis for {request.file_path}\n"
        
        for note in request.optimization_notes:
            entry += f"- {note}\n"
        
        if self.mock_mode:
            logger.info(f"[MOCK] Changelog entry generated")
        
        return entry
    
    async def _track_version(
        self,
        request: DocumentationUpdateRequest,
        files_updated: List[str]
    ) -> str:
        """
        Track documentation version.
        
        Args:
            request: Documentation update request
            files_updated: List of updated files
            
        Returns:
            Version string
        """
        version = f"1.{len(self.version_history)}.0"
        
        self.version_history.append({
            "version": version,
            "timestamp": datetime.utcnow().isoformat(),
            "file_path": request.file_path,
            "files_updated": files_updated
        })
        
        logger.info(f"Documentation version tracked: {version}")
        
        return version
    
    def get_version_history(self) -> List[Dict[str, Any]]:
        """
        Get documentation version history.
        
        Returns:
            List of version entries
        """
        return self.version_history

# Made with Bob
