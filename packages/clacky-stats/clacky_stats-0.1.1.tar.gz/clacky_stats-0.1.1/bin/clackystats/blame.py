#!/usr/bin/env python3

import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from operator import itemgetter
from typing import Dict, List, Optional, Tuple, Union

import semver
import yaml
from tqdm import tqdm

class BlameAnalyzer:
    website_files = [
        "clacky/website/share/index.md",
        "clacky/website/_includes/head_custom.html",
        "clacky/website/docs/leaderboards/index.md",
    ]

    exclude_files = [
        "clacky/website/install.ps1",
        "clacky/website/install.sh",
    ]

    hash_len = len("444444444")

    def __init__(self):
        self.repo_path = os.getcwd()

    def run(self, cmd: List[str]) -> str:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except KeyboardInterrupt:
            print("\n操作被用户中断")
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}", file=sys.stderr)
            sys.exit(1)

    def get_commit_by_date(self, date_str: str, is_end_date: bool = False) -> Optional[str]:
        try:
            commit = self.run(["git", "rev-list", "-1", "--before=" + date_str, "HEAD"]).strip()
            if not commit:
                print(f"警告: 在 {date_str} 之前没有找到任何提交")
                return None
            return commit
        except subprocess.CalledProcessError as e:
            print(f"警告: 查找日期 {date_str} 的提交时出错: {e}")
            return None

    def blame(self, start_date: Optional[str] = None, end_date: Optional[str] = None, 
             start_tag: Optional[str] = None, end_tag: Optional[str] = None) -> Tuple[Dict, defaultdict, int, int, float, datetime]:
        if start_date:
            if len(start_date.split()) == 1:
                start_date += "T00:00:00"

        if end_date:
            if len(end_date.split()) == 1:
                end_date += "T23:59:59"

        if start_date:
            start_commit = self.get_commit_by_date(start_date, is_end_date=False)
            if start_commit is None:
                return {}, defaultdict(int), 0, 0, 0, datetime.now()
        else:
            start_commit = start_tag

        if end_date:
            end_commit = self.get_commit_by_date(end_date, is_end_date=True)
            if end_commit is None:
                return {}, defaultdict(int), 0, 0, 0, datetime.now()
        else:
            end_commit = end_tag

        commits = self.get_all_commit_hashes_between_tags(start_commit, end_commit, start_date, end_date)
        if not commits:
            commits = []
        commits = [commit[:self.hash_len] for commit in commits]

        authors = self.get_commit_authors(commits)

        revision = end_commit if end_commit else "HEAD"
        files = self.run(["git", "ls-tree", "-r", "--name-only", revision]).strip().split("\n")
        test_files = [f for f in files if f.startswith("tests/fixtures/languages/") and "/test." in f]
        files = [
            f
            for f in files
            if f.endswith((".js", ".py", ".scm", ".sh", "Dockerfile", "Gemfile","ts","md","yml","json","tsx","astro","go","java"))
            or (f.startswith(".github/workflows/") and f.endswith(".yml"))
            or (f.startswith("clacky/resources/") and f.endswith(".yml"))
            or f in self.website_files
            or f in test_files
        ]
        files = [f for f in files if not f.endswith("prompts.py")]
        files = [f for f in files if not f.startswith("tests/fixtures/watch")]
        files = [f for f in files if f not in self.exclude_files]

        all_file_counts = {}
        grand_total = defaultdict(int)
        clacky_total = 0
        for file in files:
            file_counts = self.get_counts_for_file(start_commit, end_commit, authors, file, start_date, end_date)
            if file_counts:
                all_file_counts[file] = file_counts
                for author, count in file_counts.items():
                    grand_total[author] += count
                    if "clacky" in author.lower():
                        clacky_total += count

        total_lines = sum(grand_total.values())
        clacky_percentage = (clacky_total / total_lines) * 100 if total_lines > 0 else 0

        end_date = self.get_tag_date(end_commit if end_commit else "HEAD")

        return all_file_counts, grand_total, total_lines, clacky_total, clacky_percentage, end_date

    def get_all_commit_hashes_between_tags(self, start_tag: str, end_tag: Optional[str] = None,
                                         start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[str]:
        if start_date:
            cmd = ["git", "rev-list", "--all"]
            if start_date:
                cmd.append(f'--since="{start_date}"')
            if end_date:
                cmd.append(f'--until="{end_date}"')
            res = self.run(cmd)
        else:
            if end_tag:
                res = self.run(["git", "rev-list", f"{start_tag}..{end_tag}"])
            else:
                res = self.run(["git", "rev-list", f"{start_tag}..HEAD"])

        if res:
            commit_hashes = res.strip().split("\n")
            return commit_hashes
        return []

    def get_commit_authors(self, commits: List[str]) -> Dict[str, str]:
        commit_to_author = {}
        for commit in commits:
            author = self.run(["git", "show", "-s", "--format=%an", commit]).strip()
            commit_message = self.run(["git", "show", "-s", "--format=%an", commit]).strip()
            commit_to_author[commit] = commit_message
        return commit_to_author

    def get_counts_for_file(self, start_tag: str, end_tag: Optional[str], authors: Dict[str, str], 
                           fname: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[Dict[str, int]]:
        try:
            blame_cmd = ["git", "blame", "-M", "-C", "-C", "--abbrev=9"]
            
            if start_date:
                date_range = []
                if start_date:
                    date_range.append(f"--since={start_date}")
                if end_date:
                    date_range.append(f"--until={end_date}")
                else:
                    date_range.append("HEAD")
                blame_cmd.extend(date_range)
                blame_cmd.extend(["--", fname])
            else:
                if end_tag:
                    blame_cmd.extend([f"{start_tag}..{end_tag}", "--", fname])
                else:
                    blame_cmd.extend([f"{start_tag}..HEAD", "--", fname])

            text = self.run(blame_cmd)
            if not text:
                return None

            text = text.splitlines()
            line_counts = defaultdict(int)
            for line in text:
                if line.startswith("^"):
                    continue
                hsh = line[:self.hash_len]
                author = authors.get(hsh, "Unknown")
                line_counts[author] += 1

            return dict(line_counts)
        except subprocess.CalledProcessError as e:
            if "no such path" in str(e).lower():
                return None
            else:
                print(f"Warning: Unable to blame file {fname}. Error: {e}", file=sys.stderr)
                return None

    def get_all_tags_since(self, start_tag: str) -> List[str]:
        all_tags = self.run(["git", "tag", "--sort=v:refname"]).strip().split("\n")
        start_version = semver.Version.parse(start_tag[1:])
        filtered_tags = [
            tag
            for tag in all_tags
            if semver.Version.is_valid(tag[1:]) and semver.Version.parse(tag[1:]) >= start_version
        ]
        return [tag for tag in filtered_tags if tag.endswith(".0")]

    def get_tag_date(self, tag: str) -> datetime:
        """获取标签的创建日期"""
        if tag == "HEAD":
            return datetime.now()
        date_str = self.run(["git", "log", "-1", "--format=%ai", tag]).strip()
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")

    def get_latest_version_tag(self) -> Optional[str]:
        all_tags = self.run(["git", "tag", "--sort=-v:refname"]).strip().split("\n")
        for tag in all_tags:
            if semver.Version.is_valid(tag[1:]) and tag.endswith(".0"):
                return tag
        return None

    def process_all_tags_since(self, start_tag: str) -> List[Dict]:
        tags = self.get_all_tags_since(start_tag)
        results = []
        for i in tqdm(range(len(tags) - 1), desc="Processing tags"):
            start_tag, end_tag = tags[i], tags[i + 1]
            all_file_counts, grand_total, total_lines, clacky_total, clacky_percentage, end_date = self.blame(
                start_tag=start_tag, end_tag=end_tag
            )
            results.append({
                "start_tag": start_tag,
                "end_tag": end_tag,
                "end_date": end_date.strftime("%Y-%m-%d"),
                "file_counts": all_file_counts,
                "grand_total": {
                    author: count
                    for author, count in sorted(grand_total.items(), key=itemgetter(1), reverse=True)
                },
                "total_lines": total_lines,
                "clacky_total": clacky_total,
                "clacky_percentage": round(clacky_percentage, 2),
            })
        return results 