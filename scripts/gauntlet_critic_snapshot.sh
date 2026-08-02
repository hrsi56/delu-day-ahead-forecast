#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 create|verify <candidate-commit> <snapshot-path>" >&2
  exit 2
}

[[ $# -eq 3 ]] || usage

mode=$1
candidate_input=$2
snapshot_input=$3

[[ "$candidate_input" =~ ^[0-9a-f]{40,64}$ ]] || {
  echo "Candidate must be a full lowercase commit SHA, not a ref or abbreviation" >&2
  exit 1
}

case "$snapshot_input" in
  /*) ;;
  *)
    echo "Snapshot path must be absolute: $snapshot_input" >&2
    exit 1
    ;;
esac

snapshot_parent=$(cd "$(dirname "$snapshot_input")" && pwd -P) || {
  echo "Snapshot parent does not exist: $(dirname "$snapshot_input")" >&2
  exit 1
}
snapshot_path="$snapshot_parent/$(basename "$snapshot_input")"

check_snapshot() {
  local resolved_snapshot snapshot_head snapshot_tree snapshot_status snapshot_branch
  local common_dir source_repo_root

  [[ -d "$snapshot_path" ]] || {
    echo "Snapshot path does not exist: $snapshot_path" >&2
    exit 1
  }

  resolved_snapshot=$(cd "$snapshot_path" && pwd -P)

  common_dir=$(git -C "$resolved_snapshot" rev-parse --git-common-dir)
  case "$common_dir" in
    /*) ;;
    *) common_dir="$resolved_snapshot/$common_dir" ;;
  esac
  common_dir=$(cd "$common_dir" && pwd -P)
  [[ "$(basename "$common_dir")" == ".git" ]] || {
    echo "Snapshot is not a linked worktree created from a non-bare repository" >&2
    exit 1
  }
  source_repo_root=$(cd "$common_dir/.." && pwd -P)

  case "$resolved_snapshot" in
    "$source_repo_root"|"$source_repo_root"/*)
      echo "Critic snapshot must be outside the Builder repository: $resolved_snapshot" >&2
      exit 1
      ;;
  esac

  snapshot_head=$(git -C "$resolved_snapshot" rev-parse --verify HEAD)
  snapshot_tree=$(git -C "$resolved_snapshot" rev-parse --verify 'HEAD^{tree}')
  snapshot_branch=$(git -C "$resolved_snapshot" symbolic-ref -q HEAD || true)

  [[ "$snapshot_head" == "$candidate_sha" ]] || {
    echo "Candidate SHA mismatch: expected $candidate_sha, got $snapshot_head" >&2
    exit 1
  }
  [[ "$snapshot_tree" == "$candidate_tree" ]] || {
    echo "Candidate tree mismatch: expected $candidate_tree, got $snapshot_tree" >&2
    exit 1
  }
  [[ -z "$snapshot_branch" ]] || {
    echo "Critic worktree is not detached: $snapshot_branch" >&2
    exit 1
  }
  [[ ! -e "$resolved_snapshot/workbench.md" ]] || {
    echo "workbench.md must not exist in the Critic snapshot" >&2
    exit 1
  }

  git -C "$resolved_snapshot" diff --quiet
  git -C "$resolved_snapshot" diff --cached --quiet
  snapshot_status=$(git -C "$resolved_snapshot" status --porcelain=v1 --untracked-files=all --ignored=matching)
  [[ -z "$snapshot_status" ]] || {
    echo "Critic snapshot is not clean:" >&2
    echo "$snapshot_status" >&2
    exit 1
  }

  printf 'candidate_sha=%s\n' "$snapshot_head"
  printf 'tree_sha=%s\n' "$snapshot_tree"
  printf 'snapshot_path=%s\n' "$resolved_snapshot"
  printf 'workbench_absent=true\n'
  printf 'tracked_index_untracked_ignored_clean=true\n'
}

case "$mode" in
  create)
    repo_root=$(git rev-parse --show-toplevel)
    repo_root=$(cd "$repo_root" && pwd -P)
    candidate_sha=$(git -C "$repo_root" rev-parse --verify "${candidate_input}^{commit}")
    [[ "$candidate_input" == "$candidate_sha" ]] || {
      echo "Candidate must be the full resolved commit SHA: $candidate_sha" >&2
      exit 1
    }
    candidate_tree=$(git -C "$repo_root" rev-parse --verify "${candidate_sha}^{tree}")
    [[ ! -e "$snapshot_path" ]] || {
      echo "Refusing to overwrite existing snapshot path: $snapshot_path" >&2
      exit 1
    }
    case "$snapshot_path" in
      "$repo_root"|"$repo_root"/*)
        echo "Critic snapshot must be created outside the Builder repository" >&2
        exit 1
        ;;
    esac
    git -C "$repo_root" worktree add --detach "$snapshot_path" "$candidate_sha"
    check_snapshot
    ;;
  verify)
    [[ -d "$snapshot_path" ]] || {
      echo "Snapshot path does not exist: $snapshot_path" >&2
      exit 1
    }
    candidate_sha=$(git -C "$snapshot_path" rev-parse --verify "${candidate_input}^{commit}")
    [[ "$candidate_input" == "$candidate_sha" ]] || {
      echo "Candidate must be the full resolved commit SHA: $candidate_sha" >&2
      exit 1
    }
    candidate_tree=$(git -C "$snapshot_path" rev-parse --verify "${candidate_sha}^{tree}")
    check_snapshot
    ;;
  *)
    usage
    ;;
esac
