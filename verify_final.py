#!/usr/bin/env python3
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPO = "MachineLearning-Nerd/icml26-olion-hadamard-implicit-bias"
EXPECTED_FORMER = "icml26-repro-fG4nXq9Ytm-olion-hadamard-implicit-bias"
EXPECTED_EMAIL = "37579156+MachineLearning-Nerd@users.noreply.github.com"
STATUSES = {
    "C1": "TOY_SOURCE_ALGORITHM1",
    "C2": "INCONCLUSIVE_CPU_INFEASIBLE",
    "C3": "UNVERIFIED",
    "C4": "UNVERIFIED",
    "C5": "UNVERIFIED",
    "C6": "UNVERIFIED",
}


def fail(message):
    raise SystemExit("FINAL_AUDIT=FAILED " + message)


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        fail("git " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def load(relative):
    path = ROOT / relative
    if not path.is_file():
        fail("missing " + relative)
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail("invalid JSON " + relative + ": " + str(exc))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sum_file(relative, expected):
    checksum_path = ROOT / relative
    if not checksum_path.is_file():
        fail("missing checksum file " + relative)
    found = {}
    for line in checksum_path.read_text().splitlines():
        fields = line.split()
        if len(fields) >= 2:
            found[fields[1]] = fields[0]
    for name, expected_hash in expected.items():
        if found.get(name) != expected_hash:
            fail("checksum record mismatch " + relative + " " + name)
        candidates = [ROOT / name, checksum_path.parent / name]
        existing = next((candidate for candidate in candidates if candidate.is_file()), None)
        if existing is None or digest(existing) != expected_hash:
            fail("checksum mismatch " + relative + " " + name)


def main():
    required = [
        ".gitignore",
        "README.md",
        "STATUS.md",
        "AUTONOMOUS_STATE.json",
        "CLAIM_EVIDENCE.md",
        "SOURCE_AUDIT.md",
        "ENVIRONMENT.md",
        "REPORT.md",
        "AUTHOR_THANK_YOU.md",
        "CITATION.cff",
        "BRANCH_AUDIT.md",
        "branch-audit.md",
        "claims.json",
        "verify_final.py",
        "contract/live_claims.json",
        "contract/metadata.json",
        "contract/contract_manifest.json",
        "evidence/source/SHA256SUMS",
        "evidence/source/arxiv-2602.01105.pdf",
        "evidence/source/arxiv-2602.01105-source.tar.gz",
        "outputs/claim1_algorithm_toy/README.md",
        "outputs/claim1_algorithm_toy/SHA256SUMS",
        "outputs/claim1_algorithm_toy/results.json",
        "outputs/claim1_algorithm_toy/summary.json",
        "outputs/claim2_source_cpu_audit/README.md",
        "outputs/claim2_source_cpu_audit/SHA256SUMS",
        "outputs/claim2_source_cpu_audit/report.json",
        "outputs/claim2_source_cpu_audit/run.log",
        "outputs/claim2_source_cpu_audit/source_excerpt.txt",
        "src/claim1_olion_diagonal_toy.py",
        "src/claim2_gpt2_cpu_audit.py",
        "tests/test_claim1.py",
        "tests/test_claim2_source_audit.py",
        "EVIDENCE_MANIFEST.json",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            fail("missing required file " + relative)

    if git("branch", "--show-current") != "main":
        fail("current branch is not main")
    branches = git("for-each-ref", "refs/heads", "--format=%(refname:short)").splitlines()
    if branches != ["main"]:
        fail("local branches are " + repr(branches))
    if git("for-each-ref", "refs/original").strip():
        fail("refs/original remains")
    remote = git("config", "--get", "remote.origin.url").removesuffix(".git")
    if remote != "https://github.com/" + EXPECTED_REPO:
        fail("unexpected origin " + remote)
    if git("rev-parse", "origin/HEAD") != git("rev-parse", "origin/main"):
        fail("origin/HEAD does not point to origin/main")

    commits = git("log", "main", "--format=%H%x09%an%x09%ae%x09%cn%x09%ce").splitlines()
    if len(commits) < 4:
        fail("too few reachable main commits")
    for line in commits:
        fields = line.split("\t")
        if len(fields) != 5 or fields[1] != "MachineLearning-Nerd" or fields[2] != EXPECTED_EMAIL or fields[3] != "MachineLearning-Nerd" or fields[4] != EXPECTED_EMAIL:
            fail("non-canonical reachable commit identity: " + line)
    if "Co-authored-by:" in git("log", "main", "--format=%B"):
        fail("co-author trailer found")

    state = load("AUTONOMOUS_STATE.json")
    if state["github"]["repository"] != EXPECTED_REPO or state["github"]["former_repository"] != EXPECTED_FORMER:
        fail("state repository mapping mismatch")
    if state["phase"] != "published_and_verified" or state["github"]["branch"] != "main" or state["github"]["branches"] != ["main"]:
        fail("state publication metadata mismatch")
    if state["overall_verdict"] != "INCONCLUSIVE_SCOPED_TO_SOURCE_AND_BOUNDED_TOY" or state["publication_allowed"] is not False:
        fail("state publication gate mismatch")
    if state["claim_statuses"] != STATUSES:
        fail("state claim statuses mismatch")

    claims = load("claims.json")
    if claims["repository"] != EXPECTED_REPO or claims["former_repository"] != EXPECTED_FORMER:
        fail("claims repository mapping mismatch")
    if claims["overall_verdict"] != state["overall_verdict"] or claims["publication_allowed"] is not False:
        fail("claims publication gate mismatch")
    if {claim["id"]: claim["status"] for claim in claims["claims"]} != STATUSES:
        fail("claims status mismatch")

    metadata = load("contract/metadata.json")
    live_claims = load("contract/live_claims.json")
    if metadata["orid"] != "fG4nXq9Ytm" or metadata["arxiv"] != "2602.01105":
        fail("contract metadata mismatch")
    if len(live_claims) != 6 or any(claim["status"] != "unverified" for claim in live_claims):
        fail("live claim contract mismatch")

    check_sum_file(
        "evidence/source/SHA256SUMS",
        {
            "arxiv-2602.01105.pdf": "b5a0a43f3be4f22d6a6bfb947b3daf1f97b741d0d43c9c4f3f70377b241abf56",
            "arxiv-2602.01105-source.tar.gz": "a731ba5fd46583ec282df7c6df76169f96e210602d4c992adc08e0f3f4a191b0",
        },
    )
    check_sum_file(
        "outputs/claim1_algorithm_toy/SHA256SUMS",
        {
            "results.json": "4b0838e6bc448c825d069f39e4e4c763bb40fad0b191de990a8b206308e736ce",
            "summary.json": "d2144f92f9320f7a7268e4c14c423ca19cfd23c741fd84fe30b50213c34ceb13",
        },
    )
    check_sum_file(
        "outputs/claim2_source_cpu_audit/SHA256SUMS",
        {
            "report.json": "428ef8e84ea7ccec2a3a445102edaed6b490cd64ba0d2e012bdcf401a0ae16a2",
            "source_excerpt.txt": "f3ad87b4cf91096d9ff8a46d5c0e2459825d15020ae77766a12e595cec1e2969",
            "run.log": "428ef8e84ea7ccec2a3a445102edaed6b490cd64ba0d2e012bdcf401a0ae16a2",
        },
    )

    with tarfile.open(ROOT / "evidence/source/arxiv-2602.01105-source.tar.gz", "r:gz") as archive:
        members = archive.getmembers()
    if len(members) != 30 or sum(member.isfile() for member in members) != 29 or sum(member.isdir() for member in members) != 1:
        fail("unexpected source archive shape")
    for member in members:
        if member.issym() or member.islnk() or (member.isfile() and member.mode & 0o111) or member.name.startswith("/") or ".." in Path(member.name).parts:
            fail("unsafe source archive member " + member.name)
    if "OLion-arxiv.tex" not in {member.name for member in members}:
        fail("main source file missing from source archive")

    toy_results = load("outputs/claim1_algorithm_toy/results.json")
    if toy_results["gradient"] != [3, -2] or toy_results["polar_q"] != [1, -1] or toy_results["sign_s"] != [1, -1] or toy_results["x1"] != [0.9, -0.9]:
        fail("toy result mismatch")
    toy_summary = load("outputs/claim1_algorithm_toy/summary.json")
    if toy_summary["verdict"] != "toy" or toy_summary["checks"] != {"polar_is_orthogonal": True, "sign_after_orthogonalization": True, "expected_update": True}:
        fail("toy summary mismatch")

    claim2 = load("outputs/claim2_source_cpu_audit/report.json")
    if claim2["claim_id"] != 2 or claim2["verdict"] != "inconclusive" or claim2["available_compute"] != "local CPU/local GTX 1050 only" or not claim2["required_source_phrases_found"]:
        fail("Claim 2 assessment mismatch")
    if "CPU-infeasible" not in claim2["decision"]:
        fail("Claim 2 decision mismatch")

    manifest = load("EVIDENCE_MANIFEST.json")
    tracked = set(git("ls-files").splitlines())
    expected_manifest = tracked - {"AUTONOMOUS_STATE.json", "EVIDENCE_MANIFEST.json"}
    entries = {entry["path"]: entry for entry in manifest["files"]}
    if set(entries) != expected_manifest:
        fail("evidence manifest file set mismatch")
    for path, entry in entries.items():
        file_path = ROOT / path
        if entry["bytes"] != file_path.stat().st_size or entry["sha256"] != digest(file_path):
            fail("evidence manifest hash mismatch " + path)

    print(
        "FINAL_AUDIT=VERIFIED branches=1 "
        + ",".join(key + ":" + value.lower() for key, value in STATUSES.items())
        + " publication_allowed=false"
    )


if __name__ == "__main__":
    main()
