import os
import json
import unittest
import logging
from dotenv import load_dotenv
from BlaskAPIAgentManager import BlaskAPIAgent
from BlaskAPIAgentManager import PlannerTool
from BlaskAPIAgentManager import BlaskAPIAgentManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()


class TestBlaskAPIAgentManager(unittest.TestCase):
    """Tests for the BlaskAPIAgentManager package."""

    def setUp(self):
        """Set up test environment."""
        self.test_query = (
            "Show YoY growth rates for all countries, sorted by performance"
        )
        self.sample_rag_answer = """
        The US iGaming market has shown significant growth over the past few years. 
        According to research reports, several states have legalized online gambling, 
        including New Jersey, Pennsylvania, Michigan, and West Virginia.
        
        Key trends include:
        1. Mobile betting expansion
        2. Increasing merger and acquisition activity
        3. Integration of cryptocurrency payment options
        
        Revenue projections suggest continued growth through 2025.
        """

    def test_api_agent(self):
        """Test the basic API agent functionality."""
        # Skip if credentials not available
        if not os.getenv("BLASK_USERNAME") or not os.getenv("BLASK_PASSWORD"):
            self.skipTest("API credentials not available, skipping test")

        logger.info("Testing BlaskAPIAgent...")
        agent = BlaskAPIAgent(
            username=os.getenv("BLASK_USERNAME"), password=os.getenv("BLASK_PASSWORD")
        )

        auth_result = agent.authenticate()
        logger.info(f"Authentication result: {auth_result}")

        # Only continue if authentication succeeds
        if not auth_result:
            self.skipTest("Authentication failed, skipping further tests")

        swagger_data = agent.load_swagger_spec()
        logger.info(f"Swagger spec loaded: {bool(swagger_data)}")
        self.assertTrue(bool(swagger_data), "Should load swagger specification")

        summary = agent.get_endpoint_summary()
        logger.info(
            f"Retrieved {sum(len(endpoints) for endpoints in summary.values())} endpoints across {len(summary)} categories"
        )
        self.assertTrue(len(summary) > 0, "Should retrieve endpoint summary")

    def test_planner_tool(self):
        """Test the planner tool."""
        # Skip if credentials not available
        if not os.getenv("BLASK_USERNAME") or not os.getenv("BLASK_PASSWORD"):
            self.skipTest("API credentials not available, skipping test")

        logger.info("Testing PlannerTool...")
        agent = BlaskAPIAgent(
            username=os.getenv("BLASK_USERNAME"), password=os.getenv("BLASK_PASSWORD")
        )

        # Only continue if authentication succeeds
        if not agent.authenticate():
            self.skipTest("Authentication failed, skipping further tests")

        planner = PlannerTool(api_agent=agent)
        actions, explanation = planner.get_api_plan(self.test_query)

        logger.info(f"Plan explanation: {explanation}")
        logger.info(f"Planned actions: {json.dumps(actions, indent=2)}")

        self.assertIsNotNone(explanation, "Should provide a plan explanation")
        self.assertIsInstance(actions, list, "Actions should be a list")

    def test_get_api_data(self):
        """Test the get_api_data method."""
        # Skip if credentials not available
        if not os.getenv("BLASK_USERNAME") or not os.getenv("BLASK_PASSWORD"):
            self.skipTest("API credentials not available, skipping test")

        logger.info("Testing BlaskAPIAgentManager get_api_data...")
        manager = BlaskAPIAgentManager()

        # Only continue if authentication succeeds
        if not manager.api_agent.authenticate():
            self.skipTest("Authentication failed, skipping further tests")

        answer = manager.get_api_data(self.test_query)
        logger.info(f"API Data Answer: {answer}")

        self.assertIsInstance(answer, str, "Answer should be a string")
        self.assertTrue(len(answer) > 0, "Answer should not be empty")


if __name__ == "__main__":
    unittest.main()
