import sys
from typing import List

from ..kubernetes import (
    get_current_namespace,
    get_pods,
    get_events_for_pod,
    get_all_events,
    get_k8s_client
)

def list_pods_for_completion():
    """List pods for zsh completion."""
    namespace = get_current_namespace()
    pods = get_pods(namespace)
    print(" ".join(pods))
    sys.exit(0)

def display_menu(pods: List[str]) -> None:
    """Display numbered menu of pods."""
    print("Select a pod:")
    print("  0) All pods")
    for i, pod in enumerate(pods, 1):
        print(f"{i:3d}) {pod}")

def get_user_selection(max_value: int) -> int:
    """Get and validate user selection."""
    while True:
        try:
            selection = int(input(f"Enter pod number (0-{max_value}): "))
            if 0 <= selection <= max_value:
                return selection
            print(f"Invalid selection. Please enter a number between 0 and {max_value}")
        except ValueError:
            print("Please enter a valid number")

def generate_zsh_completion():
    """Generate zsh completion script."""
    script = """#compdef kge

_kge() {
    local -a pods
    pods=($(kge --complete))
    _describe 'pods' pods
}

compdef _kge kge
"""
    print(script)
    sys.exit(0)

def main():
    # Check if we can connect to Kubernetes
    try:
        get_k8s_client()
    except Exception as e:
        print(f"Error connecting to Kubernetes: {e}")
        sys.exit(1)

    # Check if we're being called for completion
    if len(sys.argv) > 1:
        if sys.argv[1] == "--complete":
            list_pods_for_completion()
        elif sys.argv[1] == "--completion=zsh":
            generate_zsh_completion()

    # Get current namespace
    namespace = get_current_namespace()
    print(f"Current namespace: {namespace}")

    # Handle -A flag for all events
    if len(sys.argv) > 1 and sys.argv[1] == "-A":
        print("Getting events for all pods")
        print("-" * 40)
        try:
            events = get_all_events(namespace)
            print(events)
            sys.exit(0)
        except Exception as e:
            print(f"Error getting events: {e}")
            sys.exit(1)

    # If a pod name is provided as a direct argument
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        pod_name = sys.argv[1]
        print(f"Getting events for pod: {pod_name}")
        print("-" * 40)
        try:
            events = get_events_for_pod(namespace, pod_name)
            print(events)
            sys.exit(0)
        except Exception as e:
            print(f"Error getting events: {e}")
            sys.exit(1)

    # Normal interactive execution
    print("Fetching pods...")
    try:
        pods = get_pods(namespace)
        if not pods:
            print(f"No pods found in namespace {namespace}")
            sys.exit(1)

        display_menu(pods)
        selection = get_user_selection(len(pods))
        
        if selection == 0:
            print("\nGetting events for all pods")
            print("-" * 40)
            events = get_all_events(namespace)
            print(events)
        else:
            selected_pod = pods[selection - 1]
            print(f"\nGetting events for pod: {selected_pod}")
            print("-" * 40)
            events = get_events_for_pod(namespace, selected_pod)
            print(events)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 