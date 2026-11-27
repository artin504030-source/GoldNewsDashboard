import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "news": "Gold News Bot",
    "prices": "Gold Prices Bot",
    "market": "Gold Market Telegram Delivery",
    "analyst": "Gold News Analyst",
    "reports": "Gold Reports Bot",
    "priced-in": "Gold Priced-In Analyst",
}


class RuntimeDashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.script = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
        cls.status = json.loads((ROOT / "bot_status.json").read_text(encoding="utf-8"))

    def test_all_six_bot_cards_exist(self):
        for key in EXPECTED:
            with self.subTest(bot=key):
                self.assertIn(f'id="runtime-{key}-badge"', self.html)
                self.assertIn(f'id="runtime-{key}-time"', self.html)
                self.assertIn(f'id="runtime-{key}-detail"', self.html)
                self.assertIn(f'id="runtime-{key}-link"', self.html)

    def test_all_six_cards_map_to_real_workflow_names(self):
        for key, workflow in EXPECTED.items():
            with self.subTest(bot=key):
                self.assertIn(f"name:'{workflow}'", self.script)
                self.assertIn(workflow, self.status.get("workflows", {}))

    def test_event_driven_analyst_is_not_marked_late_by_idle_time(self):
        self.assertRegex(
            self.script,
            re.compile(r"analyst:\{id:'runtime-analyst',name:'Gold News Analyst',staleMinutes:null\}")
        )
        self.assertIn("cfg.staleMinutes!=null&&age>cfg.staleMinutes", self.script)

    def test_supporting_workflows_remain_in_status_feed(self):
        workflows = self.status.get("workflows", {})
        self.assertIn("Gold News Breaking Monitor", workflows)
        self.assertIn("Gold News Daily Digest", workflows)


if __name__ == "__main__":
    unittest.main()
