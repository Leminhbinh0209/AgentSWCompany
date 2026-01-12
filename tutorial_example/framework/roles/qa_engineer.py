"""QA Engineer role"""
from framework.role import Role
from framework.actions.write_test import WriteTest, RunTest, ReportBugs


class QAEngineer(Role):
    """QA Engineer role for testing and quality assurance"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="QAEngineer",
            profile="QA Engineer",
            goal="Ensure code quality through comprehensive testing and bug reporting",
            actions=[WriteTest(llm=llm), RunTest(llm=llm), ReportBugs(llm=llm)],
            llm=llm
        )
    
    async def generate_tests(self, code: str) -> str:
        """
        Generate tests for code
        
        Args:
            code: Code to test
            
        Returns:
            Test code
        """
        from framework.schema import Message
        write_test_action = next((a for a in self.actions if isinstance(a, WriteTest)), None)
        if write_test_action:
            messages = [Message(content=code, role="Engineer", cause_by="WriteCode")]
            result = await write_test_action.run(messages=messages)
            return result.content
        return ""
    
    async def run_tests(self, test_file: str) -> dict:
        """
        Run tests
        
        Args:
            test_file: Path to test file
            
        Returns:
            Test results
        """
        run_test_action = next((a for a in self.actions if isinstance(a, RunTest)), None)
        if run_test_action:
            result = await run_test_action.run(test_file=test_file)
            return result.instruct_content.get("results", {})
        return {}
    
    async def report_bugs(self, test_results: str) -> str:
        """
        Generate bug report
        
        Args:
            test_results: Test execution results
            
        Returns:
            Bug report
        """
        from framework.schema import Message
        report_bugs_action = next((a for a in self.actions if isinstance(a, ReportBugs)), None)
        if report_bugs_action:
            messages = [Message(content=test_results, role="QAEngineer", cause_by="RunTest")]
            result = await report_bugs_action.run(messages=messages)
            return result.content
        return ""

