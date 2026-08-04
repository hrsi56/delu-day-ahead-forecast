#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage:" >&2
  echo "  $0 create <candidate-commit> <snapshot-path> <manifest-path> <critic-run-id>" >&2
  echo "  $0 verify <candidate-commit> <snapshot-path> <manifest-path> <pre-review-manifest-sha256>" >&2
  exit 2
}

[[ $# -eq 5 ]] || usage

mode=$1
candidate_input=$2
snapshot_input=$3
manifest_input=$4
mode_input=$5

[[ "$candidate_input" =~ ^([0-9a-f]{40}|[0-9a-f]{64})$ ]] || {
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

case "$manifest_input" in
  /*) ;;
  *)
    echo "Integrity manifest path must be absolute: $manifest_input" >&2
    exit 1
    ;;
esac

snapshot_parent=$(cd "$(dirname "$snapshot_input")" && pwd -P) || {
  echo "Snapshot parent does not exist: $(dirname "$snapshot_input")" >&2
  exit 1
}
snapshot_path="$snapshot_parent/$(basename "$snapshot_input")"

manifest_parent=$(cd "$(dirname "$manifest_input")" && pwd -P) || {
  echo "Integrity manifest parent does not exist: $(dirname "$manifest_input")" >&2
  exit 1
}
manifest_path="$manifest_parent/$(basename "$manifest_input")"

case "$manifest_path" in
  "$snapshot_path"|"$snapshot_path"/*)
    echo "Integrity manifest must be outside the Critic snapshot" >&2
    exit 1
    ;;
esac

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd -P)
snapshot_helper_path="$script_dir/gauntlet_critic_snapshot.sh"
protocol_tool="$script_dir/gauntlet_protocol.py"
python_bin=${PYTHON_BIN:-python3}
command -v "$python_bin" >/dev/null 2>&1 || {
  echo "Python interpreter not found: $python_bin" >&2
  exit 1
}
[[ -f "$protocol_tool" ]] || {
  echo "Gauntlet protocol helper not found: $protocol_tool" >&2
  exit 1
}
[[ -f "$snapshot_helper_path" ]] || {
  echo "Snapshot helper not found: $snapshot_helper_path" >&2
  exit 1
}
snapshot_helper_sha256=$(
  "$python_bin" -c 'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' "$snapshot_helper_path"
)
protocol_helper_sha256=$(
  "$python_bin" -c 'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' "$protocol_tool"
)

check_snapshot() {
  local resolved_snapshot snapshot_status snapshot_branch
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

  verified_head=$(git -C "$resolved_snapshot" rev-parse --verify HEAD)
  verified_tree=$(git -C "$resolved_snapshot" rev-parse --verify 'HEAD^{tree}')
  snapshot_branch=$(git -C "$resolved_snapshot" symbolic-ref -q HEAD || true)

  [[ "$verified_head" == "$candidate_sha" ]] || {
    echo "Candidate SHA mismatch: expected $candidate_sha, got $verified_head" >&2
    exit 1
  }
  [[ "$verified_tree" == "$candidate_tree" ]] || {
    echo "Candidate tree mismatch: expected $candidate_tree, got $verified_tree" >&2
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

  git -C "$resolved_snapshot" diff --quiet --exit-code
  git -C "$resolved_snapshot" diff --cached --quiet --exit-code
  snapshot_status=$(git -C "$resolved_snapshot" status --porcelain=v1 --untracked-files=all --ignored=matching)
  [[ -z "$snapshot_status" ]] || {
    echo "Critic snapshot is not clean:" >&2
    echo "$snapshot_status" >&2
    exit 1
  }

  verified_snapshot_path=$resolved_snapshot
}

print_snapshot_evidence() {
  printf 'candidate_sha=%s\n' "$verified_head"
  printf 'tree_sha=%s\n' "$verified_tree"
  printf 'snapshot_path=%s\n' "$verified_snapshot_path"
  printf 'workbench_absent=true\n'
  printf 'tracked_index_untracked_ignored_clean=true\n'
}

case "$mode" in
  create)
    [[ "$mode_input" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]] || {
      echo "Critic run ID contains unsupported characters: $mode_input" >&2
      exit 1
    }
    [[ "$(basename "$manifest_path")" == "integrity-manifest.json" ]] || {
      echo "Integrity manifest filename must be integrity-manifest.json" >&2
      exit 1
    }
    [[ ! -e "$manifest_path" && ! -L "$manifest_path" ]] || {
      echo "Refusing to overwrite existing integrity manifest: $manifest_path" >&2
      exit 1
    }
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
    pre_review_manifest_sha256=$(
      "$python_bin" "$protocol_tool" _manifest-create \
        --manifest "$manifest_path" \
        --run-id "$mode_input" \
        --candidate-sha "$verified_head" \
        --candidate-tree "$verified_tree" \
        --snapshot-path "$verified_snapshot_path" \
        --snapshot-helper-path "$snapshot_helper_path" \
        --snapshot-helper-sha256 "$snapshot_helper_sha256" \
        --protocol-helper-path "$protocol_tool" \
        --protocol-helper-sha256 "$protocol_helper_sha256"
    )
    print_snapshot_evidence
    printf 'critic_run_id=%s\n' "$mode_input"
    printf 'integrity_manifest_path=%s\n' "$manifest_path"
    printf 'pre_review_manifest_sha256=%s\n' "$pre_review_manifest_sha256"
    ;;
  verify)
    [[ "$mode_input" =~ ^[0-9a-f]{64}$ ]] || {
      echo "Pre-review integrity manifest SHA-256 must be 64 lowercase hex characters" >&2
      exit 1
    }
    [[ -f "$manifest_path" && ! -L "$manifest_path" ]] || {
      echo "Integrity manifest does not exist or is a symlink: $manifest_path" >&2
      exit 1
    }
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
    final_manifest_sha256=$(
      "$python_bin" "$protocol_tool" _manifest-verify \
        --manifest "$manifest_path" \
        --pre-review-sha256 "$mode_input" \
        --candidate-sha "$verified_head" \
        --candidate-tree "$verified_tree" \
        --snapshot-path "$verified_snapshot_path" \
        --snapshot-helper-path "$snapshot_helper_path" \
        --snapshot-helper-sha256 "$snapshot_helper_sha256" \
        --protocol-helper-path "$protocol_tool" \
        --protocol-helper-sha256 "$protocol_helper_sha256"
    )
    print_snapshot_evidence
    printf 'integrity_manifest_path=%s\n' "$manifest_path"
    printf 'final_integrity_manifest_sha256=%s\n' "$final_manifest_sha256"
    ;;
  *)
    usage
    ;;
esac
