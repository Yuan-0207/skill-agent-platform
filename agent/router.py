"""
技能路由器：扫描 skills/**/SKILL.md，按 triggers 匹配用户输入。
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class SkillRoute:
    skill_id: str
    skill_name: str
    description: str
    tools: list[str]
    priority: int
    response_template: str
    skill_dir: Path


class SkillRouter:
    def __init__(self, skills_root: Path):
        self._skills_root = skills_root
        self._skills: list[SkillRoute] = []
        self._load_all()

    def _load_all(self) -> None:
        if not self._skills_root.exists():
            return
        for skill_md in sorted(self._skills_root.glob("*/SKILL.md")):
            parsed = self._parse_skill_md(skill_md)
            if parsed:
                self._skills.append(parsed)
        self._skills.sort(key=lambda s: s.priority, reverse=True)

    def _parse_skill_md(self, path: Path) -> SkillRoute | None:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None
        parts = text.split("---", 2)
        if len(parts) < 3:
            return None
        meta = yaml.safe_load(parts[1]) or {}
        if not meta.get("id"):
            return None
        return SkillRoute(
            skill_id=str(meta["id"]),
            skill_name=str(meta.get("name", meta["id"])),
            description=str(meta.get("description", "")),
            tools=list(meta.get("tools") or []),
            priority=int(meta.get("priority") or 0),
            response_template=str(meta.get("response_template") or "{result}"),
            skill_dir=path.parent,
        )

    def route(self, message: str) -> SkillRoute | None:
        msg = message.strip().lower()
        if not msg:
            return None
        best: SkillRoute | None = None
        best_score = 0
        for skill in self._skills:
            score = 0
            for trigger in self._triggers_for(skill):
                if trigger in msg:
                    score += len(trigger) + skill.priority
            if score > best_score:
                best_score = score
                best = skill
        return best

    def _triggers_for(self, skill: SkillRoute) -> list[str]:
        path = skill.skill_dir / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return []
        parts = text.split("---", 2)
        meta = yaml.safe_load(parts[1]) or {}
        return [str(t).lower() for t in (meta.get("triggers") or [])]

    def list_skills(self) -> list[dict]:
        return [
            {
                "id": s.skill_id,
                "name": s.skill_name,
                "tools": s.tools,
                "priority": s.priority,
            }
            for s in self._skills
        ]
