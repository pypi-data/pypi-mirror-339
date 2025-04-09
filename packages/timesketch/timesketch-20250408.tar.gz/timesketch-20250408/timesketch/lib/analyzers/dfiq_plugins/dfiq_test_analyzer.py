"""Test DFIQ analyzer"""

import logging

from timesketch.lib.analyzers import interface

logger = logging.getLogger("timesketch.analyzers.dfiq.test")


class DFIQTestAnalyzer(interface.BaseAnalyzer):
    """Analyzer to test the DFIQ analyzer functionallity!"""

    NAME = "dfiq_test_analyzer"
    DISPLAY_NAME = "DFIQ Test Analyzer"
    DESCRIPTION = "This is a test DFIQ Analyzer"
    IS_DFIQ_ANALYZER = True

    # Add DFIQ-specific metadata
    DFIQ_ID = "Q1002"  # Optional: Link to the specific DFIQ
    DFIQ_UUID = "" # Optional: Link to specific DFIQ UUID
    DFIQ_APPROACH = "Analyze files on USB..."  # Approach name (optional)
    REQUIRED_DATA_TYPES = []  # Data type dependency
    DEPENDENCIES = frozenset()

    def __init__(self, index_name, sketch_id, timeline_id=None):
        # DFIQ Analyzers should not be listed in the general analyzer list.
        self.index_name = index_name
        super().__init__(index_name, sketch_id, timeline_id=timeline_id)

    def run(self):
        """Entry point for the dfiq analyzer.

        Returns:
            Output object containing all relevant information and a verdict.
        """
        # Query to run!
        query = (
            "_exists_:hash_sha256 OR _exists_:sha256 OR _exists_:hash OR "
            "_exists_:sha256_hash"
        )

        # Define return fields used for your analysis!
        return_fields = ["hash_sha256", "hash", "sha256", "sha256_hash"]

        # Generator of events based on your query.
        # Swap for self.event_pandas to get pandas back instead of events.
        events = self.event_stream(query_string=query, return_fields=return_fields)

        # 1. Data Enhancement & Filtering (if applicable)
        for event in events:
            # ... add tags, enrich data, etc.
            pass
            #event.add_tags(["sha256"])

        self.output.result_status = "SUCCESS"
        self.output.result_priority = "NOTE"
        self.output.result_summary = "This is a test verdict for the DFIQ analyzer!"

        return str(self.output)
