import requests
import time

# Roblox Friends API URL
ROBLOX_FRIENDS_API = "https://friends.roblox.com/v1/users/{}/friends?limit=100&cursor={}"

def get_friends(user_id):
    """
    Scrapes and prints all friends of a Roblox user, handling pagination.

    Args:
        user_id (int): The Roblox user ID.
    """
    cursor = ""  # Start with an empty cursor to fetch the first batch
    all_usernames = []  # List to store all friends' usernames
    while cursor is not None:
        url = ROBLOX_FRIENDS_API.format(user_id, cursor)
        print(f"🔍 Fetching page with cursor: {cursor}")  # Debugging line to track pagination
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            friends = data.get("data", [])
            if not friends:
                print("⚠️ No friends found or the list is private.")
                break

            # Add current batch of friends to the list
            all_usernames.extend(friend["name"] for friend in friends)

            # Get the cursor for the next page of results
            cursor = data.get("nextPageCursor")

            # Display progress and delay for each batch
            print(f"\n✅ Found {len(friends)} more friends. Total friends so far: {len(all_usernames)}")
            time.sleep(0.5)  # Small delay to prevent rate limits
        else:
            print(f"❌ Failed to fetch friends. Invalid User ID or private profile.")
            break

    # Display all found usernames
    print(f"\n✅ Total {len(all_usernames)} friends found:\n")
    for i, username in enumerate(all_usernames, start=1):
        print(f"[{i}] {username}")

    # Save to a file
    with open("roblox_friends.txt", "w") as f:
        for username in all_usernames:
            f.write(username + "\n")

    print("\n📂 Usernames saved to roblox_friends.txt")

# Ask for a User ID
user_id = input("Enter the Roblox User ID to scrape: ").strip()

# Validate input
if not user_id.isdigit():
    print("❌ Invalid User ID! Please enter a number.")
else:
    user_id = int(user_id)  # Convert input to integer
    print("\n🔍 Fetching friends list...\n")
    get_friends(user_id)
