#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp[cli]>=1.6.0",
# ]
# ///

import json
import os
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("QAnon Posts Explorer")

# Path to the dataset
DATASET_FILENAME = "posts.json"


# Load the dataset
def load_dataset():
    # Get the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create path to dataset relative to script
    dataset_path = os.path.join(script_dir, DATASET_FILENAME)

    try:
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("posts", [])
    except FileNotFoundError:
        print(f"Error: Dataset file '{dataset_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from '{dataset_path}'.")
        return []


# Cache the dataset
posts = load_dataset()


# Helper functions
def get_post_by_id(post_id: int) -> Optional[Dict]:
    """Get a post by its ID."""
    for post in posts:
        if post.get("post_metadata", {}).get("id") == post_id:
            return post
    return None


def search_posts_by_keyword(keyword: str) -> List[Dict]:
    """Search posts containing a keyword."""
    keyword = keyword.lower()
    results = []
    for post in posts:
        text = post.get("text", "").lower()
        if keyword in text:
            results.append(post)
    return results


def get_posts_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """Get posts within a date range (YYYY-MM-DD format)."""
    try:
        start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        end_timestamp = (
            int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()) + 86400
        )  # Add a day in seconds

        results = []
        for post in posts:
            post_time = post.get("post_metadata", {}).get("time", 0)
            if start_timestamp <= post_time <= end_timestamp:
                results.append(post)
        return results
    except ValueError:
        return []


def get_posts_by_author(author: str) -> List[Dict]:
    """Get posts by a specific author."""
    results = []
    for post in posts:
        post_author = post.get("post_metadata", {}).get("author", "")
        if post_author.lower() == author.lower():
            results.append(post)
    return results


def format_post(post: Dict) -> str:
    """Format a post for display."""
    metadata = post.get("post_metadata", {})
    post_id = metadata.get("id", "Unknown")
    author = metadata.get("author", "Unknown")
    author_id = metadata.get("author_id", "Unknown")
    tripcode = metadata.get("tripcode", "Unknown")

    source = metadata.get("source", {})
    board = source.get("board", "Unknown")
    site = source.get("site", "Unknown")

    timestamp = metadata.get("time", 0)
    date_str = (
        datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        if timestamp
        else "Unknown"
    )

    text = post.get("text", "")
    if text:
        # Replace '\n' string literals with actual newlines
        text = text.replace("\\n", "\n")

    # Format images
    images_section = ""
    images = post.get("images", [])
    if images:
        images_section = "\nImages:\n"
        for img in images:
            images_section += f"- File: {img.get('file', 'Unknown')}, Name: {img.get('name', 'Unknown')}\n"

    # Format referenced posts
    refs_section = ""
    refs = post.get("referenced_posts", [])
    if refs:
        refs_section = "\nReferenced Posts:\n"
        for ref in refs:
            ref_text = ref.get("text", "No text")
            if ref_text:
                ref_text = ref_text.replace("\\n", "\n")
            ref_author_id = ref.get("author_id", "Unknown")
            refs_section += f"- Reference: {ref.get('reference', 'Unknown')}\n"
            refs_section += f"  Author ID: {ref_author_id}\n"
            refs_section += f"  Text: {ref_text}\n"

    # Assemble the formatted post
    formatted = f"""
Post ID: {post_id}
Author: {author} (ID: {author_id}, tripcode: {tripcode})
Source: {board} on {site}
Date: {date_str}
Text:
{text}
{images_section}
{refs_section}
"""
    return formatted.strip()


# Resources


@mcp.resource("qanon://posts/count")
def get_posts_count() -> str:
    """Get the total number of posts in the dataset."""
    return str(len(posts))


@mcp.resource("qanon://posts/{post_id}")
def get_post_resource(post_id: int) -> str:
    """Get a specific post by ID."""
    post = get_post_by_id(post_id)
    if post:
        return format_post(post)
    return "Post not found."


@mcp.resource("qanon://posts/raw/{post_id}")
def get_raw_post_resource(post_id: int) -> str:
    """Get a specific post by ID with all raw fields in JSON format."""
    post = get_post_by_id(post_id)
    if post:
        return json.dumps(post, indent=2)
    return "Post not found."


@mcp.resource("qanon://authors")
def get_authors() -> str:
    """Get a list of unique authors in the dataset."""
    authors = set()
    for post in posts:
        author = post.get("post_metadata", {}).get("author", "")
        if author:
            authors.add(author)
    return "\n".join(sorted(authors))


@mcp.resource("qanon://stats")
def get_stats() -> str:
    """Get general statistics about the dataset."""
    if not posts:
        return "No posts found in the dataset."

    # Count posts by author
    author_counts = {}
    # Count posts by site
    site_counts = {}
    # Count posts by board
    board_counts = {}
    # Count posts with images
    image_count = 0
    # Count posts with references
    ref_count = 0
    # Find earliest and latest dates
    earliest_time = float("inf")
    latest_time = 0

    for post in posts:
        # Author counts
        author = post.get("post_metadata", {}).get("author", "Unknown")
        author_counts[author] = author_counts.get(author, 0) + 1

        # Site counts
        site = post.get("post_metadata", {}).get("source", {}).get("site", "Unknown")
        site_counts[site] = site_counts.get(site, 0) + 1

        # Board counts
        board = post.get("post_metadata", {}).get("source", {}).get("board", "Unknown")
        board_counts[board] = board_counts.get(board, 0) + 1

        # Image count
        if post.get("images"):
            image_count += 1

        # Reference count
        if post.get("referenced_posts"):
            ref_count += 1

        # Time range
        time_val = post.get("post_metadata", {}).get("time", 0)
        if time_val:
            earliest_time = min(earliest_time, time_val)
            latest_time = max(latest_time, time_val)

    # Format dates
    earliest_date = (
        datetime.fromtimestamp(earliest_time).strftime("%Y-%m-%d")
        if earliest_time != float("inf")
        else "Unknown"
    )
    latest_date = (
        datetime.fromtimestamp(latest_time).strftime("%Y-%m-%d")
        if latest_time
        else "Unknown"
    )

    # Format output
    result = f"""
QAnon Posts/Drops Dataset Statistics:

Total Posts/Drops: {len(posts)}
Date Range: {earliest_date} to {latest_date}
Posts/Drops with Images: {image_count}
Posts/Drops with Referenced Posts: {ref_count}

Top Authors:
"""

    for author, count in sorted(
        author_counts.items(), key=lambda x: x[1], reverse=True
    ):
        result += f"- {author}: {count} posts\n"

    result += "\nPosts by Site:\n"
    for site, count in sorted(site_counts.items(), key=lambda x: x[1], reverse=True):
        result += f"- {site}: {count} posts\n"

    result += "\nPosts by Board:\n"
    for board, count in sorted(board_counts.items(), key=lambda x: x[1], reverse=True):
        result += f"- {board}: {count} posts\n"

    return result.strip()


# Tools


@mcp.tool()
def get_post_by_id_tool(post_id: int) -> str:
    """
    Retrieve a specific post by its ID.

    Args:
        post_id: The ID of the post to retrieve
    """
    # Use the existing helper function to get the post
    post = get_post_by_id(post_id)

    if not post:
        return f"Post with ID {post_id} not found."

    # Use the existing format_post function to format the output
    formatted_post = format_post(post)

    # Get adjacent posts for context
    post_list = sorted(posts, key=lambda x: x.get("post_metadata", {}).get("id", 0))
    post_ids = [p.get("post_metadata", {}).get("id", 0) for p in post_list]

    try:
        index = post_ids.index(post_id)
        context = "\nAdjacent Posts:\n"

        # Get previous post if it exists
        if index > 0:
            prev_id = post_ids[index - 1]
            prev_date = datetime.fromtimestamp(
                post_list[index - 1].get("post_metadata", {}).get("time", 0)
            ).strftime("%Y-%m-%d")
            context += f"Previous post: #{prev_id} from {prev_date}\n"

        # Get next post if it exists
        if index < len(post_ids) - 1:
            next_id = post_ids[index + 1]
            next_date = datetime.fromtimestamp(
                post_list[index + 1].get("post_metadata", {}).get("time", 0)
            ).strftime("%Y-%m-%d")
            context += f"Next post: #{next_id} from {next_date}\n"
    except ValueError:
        context = ""

    result = f"Post #{post_id}:\n\n{formatted_post}\n{context}"

    return result


@mcp.tool()
def search_posts(query: str, limit: int = 10) -> str:
    """
    Search for posts/drops containing a specific keyword or phrase.

    Args:
        query: The keyword or phrase to search for
        limit: Maximum number of results to return (default: 10)
    """
    if not query:
        return "Please provide a search query."

    results = search_posts_by_keyword(query)

    if not results:
        return f"No posts found containing '{query}'."

    total_found = len(results)
    results = results[:limit]

    output = f"Found {total_found} posts containing '{query}'. Showing top {len(results)} results:\n\n"

    for i, post in enumerate(results, 1):
        output += f"Result {i}:\n{format_post(post)}\n\n" + "-" * 40 + "\n\n"

    if total_found > limit:
        output += f"... and {total_found - limit} more posts."

    return output


@mcp.tool()
def get_posts_by_date(start_date: str, end_date: str = None, limit: int = 10) -> str:
    """
    Get posts/drops within a specific date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format (defaults to start_date if not provided)
        limit: Maximum number of results to return (default: 10)
    """
    if not end_date:
        end_date = start_date

    try:
        # Validate date format
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

    results = get_posts_by_date_range(start_date, end_date)

    if not results:
        return f"No posts found between {start_date} and {end_date}."

    total_found = len(results)
    results = results[:limit]

    output = f"Found {total_found} posts between {start_date} and {end_date}. Showing top {len(results)} results:\n\n"

    for i, post in enumerate(results, 1):
        output += f"Result {i}:\n{format_post(post)}\n\n" + "-" * 40 + "\n\n"

    if total_found > limit:
        output += f"... and {total_found - limit} more posts."

    return output


@mcp.tool()
def get_posts_by_author_id(author_id: str, limit: int = 10) -> str:
    """
    Get posts/drops by a specific author ID.

    Args:
        author_id: The author ID to search for
        limit: Maximum number of results to return (default: 10)
    """
    if not author_id:
        return "Please provide an author ID."

    results = []
    for post in posts:
        post_author_id = post.get("post_metadata", {}).get("author_id", "")
        if post_author_id == author_id:
            results.append(post)

    if not results:
        return f"No posts found with author ID '{author_id}'."

    total_found = len(results)
    results = results[:limit]

    output = f"Found {total_found} posts with author ID '{author_id}'. Showing top {len(results)} results:\n\n"

    for i, post in enumerate(results, 1):
        output += f"Result {i}:\n{format_post(post)}\n\n" + "-" * 40 + "\n\n"

    if total_found > limit:
        output += f"... and {total_found - limit} more posts."

    return output


@mcp.tool()
def analyze_post(post_id: int) -> str:
    """
    Get detailed analysis of a specific post/drop including references and context.

    Args:
        post_id: The ID of the post to analyze
    """
    post = get_post_by_id(post_id)
    if not post:
        return f"Post with ID {post_id} not found."

    metadata = post.get("post_metadata", {})
    author = metadata.get("author", "Unknown")
    author_id = metadata.get("author_id", "Unknown")
    timestamp = metadata.get("time", 0)
    date_str = (
        datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        if timestamp
        else "Unknown"
    )

    source = metadata.get("source", {})
    board = source.get("board", "Unknown")
    site = source.get("site", "Unknown")
    link = source.get("link", "Unknown")

    text = post.get("text", "")
    if text:
        text = text.replace("\\n", "\n")

    # Images analysis
    images = post.get("images", [])
    images_analysis = ""
    if images:
        images_analysis = f"\n\nImages ({len(images)}):\n"
        for i, img in enumerate(images, 1):
            images_analysis += f"{i}. File: {img.get('file', 'Unknown')}, Name: {img.get('name', 'Unknown')}\n"

    # Referenced posts analysis
    refs = post.get("referenced_posts", [])
    refs_analysis = ""
    if refs:
        refs_analysis = f"\n\nReferenced Posts ({len(refs)}):\n"
        for i, ref in enumerate(refs, 1):
            ref_text = ref.get("text", "No text")
            if ref_text:
                ref_text = ref_text.replace("\\n", "\n")
            ref_author_id = ref.get("author_id", "Unknown")
            refs_analysis += f"{i}. Reference: {ref.get('reference', 'Unknown')}\n"
            refs_analysis += f"   Author ID: {ref_author_id}\n"
            refs_analysis += f"   Text: {ref_text}\n\n"

    # Find other posts by the same author
    same_author_posts = get_posts_by_author_id(author_id, limit=5)

    # Build the analysis
    analysis = f"""
Detailed Analysis of Post/Drop {post_id}:

Basic Information:
-----------------
Author: {author} (ID: {author_id})
Date: {date_str}
Source: {board} on {site}
Original Link: {link}

Post Content:
------------
{text}
{images_analysis}
{refs_analysis}

Context:
-------
This post is part of {len(posts)} total posts in the dataset.
"""

    # Add information about posts around this one
    post_position = None
    for i, p in enumerate(
        sorted(posts, key=lambda x: x.get("post_metadata", {}).get("id", 0))
    ):
        if p.get("post_metadata", {}).get("id") == post_id:
            post_position = i
            break

    if post_position is not None:
        analysis += f"\nThis is post #{post_position + 1} in chronological order.\n"

        # Previous post
        if post_position > 0:
            prev_post = posts[post_position - 1]
            prev_id = prev_post.get("post_metadata", {}).get("id", "Unknown")
            prev_date = datetime.fromtimestamp(
                prev_post.get("post_metadata", {}).get("time", 0)
            ).strftime("%Y-%m-%d")
            analysis += f"\nPrevious post: #{prev_id} from {prev_date}\n"

        # Next post
        if post_position < len(posts) - 1:
            next_post = posts[post_position + 1]
            next_id = next_post.get("post_metadata", {}).get("id", "Unknown")
            next_date = datetime.fromtimestamp(
                next_post.get("post_metadata", {}).get("time", 0)
            ).strftime("%Y-%m-%d")
            analysis += f"Next post: #{next_id} from {next_date}\n"

    return analysis


@mcp.tool()
def get_timeline_summary(start_date: str = None, end_date: str = None) -> str:
    """
    Get a timeline summary of posts/drops, optionally within a date range.

    Args:
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format
    """
    # Use all posts if no dates provided
    timeline_posts = posts

    # Filter by date range if provided
    if start_date and end_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            timeline_posts = get_posts_by_date_range(start_date, end_date)
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD format."

    # Sort posts by time
    timeline_posts = sorted(
        timeline_posts, key=lambda x: x.get("post_metadata", {}).get("time", 0)
    )

    if not timeline_posts:
        return "No posts found for the specified date range."

    # Group posts by month
    months = {}
    for post in timeline_posts:
        timestamp = post.get("post_metadata", {}).get("time", 0)
        if timestamp:
            month_key = datetime.fromtimestamp(timestamp).strftime("%Y-%m")
            if month_key not in months:
                months[month_key] = []
            months[month_key].append(post)

    # Build the timeline
    timeline = "QAnon Posts Timeline:\n\n"

    for month_key in sorted(months.keys()):
        month_name = datetime.strptime(month_key, "%Y-%m").strftime("%B %Y")
        month_posts = months[month_key]

        timeline += f"## {month_name} ({len(month_posts)} posts)\n\n"

        # Get the first and last 2 posts of the month as examples
        sample_posts = []
        if len(month_posts) <= 4:
            sample_posts = month_posts
        else:
            sample_posts = month_posts[:2] + month_posts[-2:]

        for post in sample_posts:
            post_id = post.get("post_metadata", {}).get("id", "Unknown")
            timestamp = post.get("post_metadata", {}).get("time", 0)
            day = datetime.fromtimestamp(timestamp).strftime("%d %b")

            text = post.get("text", "")
            if text:
                text = text.replace("\\n", " ")
                # Truncate text if too long
                if len(text) > 100:
                    text = text[:97] + "..."

            timeline += f"- {day}: Post #{post_id} - {text}\n"

        if len(month_posts) > 4:
            timeline += f"  ... and {len(month_posts) - 4} more posts this month\n"

        timeline += "\n"

    return timeline


def generate_word_cloud(
    post_texts: List[str], min_word_length: int = 3, max_words: int = 100
) -> str:
    """
    Generate a word cloud analysis from a list of post texts.

    Args:
        post_texts: List of text content from posts
        min_word_length: Minimum length of words to include (default: 3)
        max_words: Maximum number of words to return (default: 100)

    Returns:
        Formatted string with word frequency analysis
    """
    # Common words to exclude (stopwords)
    stopwords = {
        "the",
        "and",
        "a",
        "to",
        "of",
        "in",
        "is",
        "that",
        "for",
        "on",
        "with",
        "as",
        "by",
        "at",
        "from",
        "be",
        "this",
        "was",
        "are",
        "an",
        "it",
        "not",
        "or",
        "have",
        "has",
        "had",
        "but",
        "what",
        "all",
        "were",
        "when",
        "there",
        "can",
        "been",
        "one",
        "do",
        "did",
        "who",
        "you",
        "your",
        "they",
        "their",
        "them",
        "will",
        "would",
        "could",
        "should",
        "which",
        "his",
        "her",
        "she",
        "he",
        "we",
        "our",
        "us",
        "i",
        "me",
        "my",
        "im",
        "ive",
        "myself",
        "its",
        "it's",
        "about",
        "some",
        "then",
        "than",
        "into",
    }

    # Combine all texts and replace literal \n with actual newlines
    combined_text = " ".join([text.replace("\\n", " ") for text in post_texts if text])

    # Remove URLs
    combined_text = re.sub(r"https?://\S+", "", combined_text)

    # Remove special characters and convert to lowercase
    combined_text = re.sub(r"[^\w\s]", " ", combined_text.lower())

    # Split into words and count frequencies
    words = combined_text.split()

    # Filter out stopwords and short words
    filtered_words = [
        word for word in words if word not in stopwords and len(word) >= min_word_length
    ]

    # Count word frequencies
    word_counts = Counter(filtered_words)

    # Get the most common words
    most_common = word_counts.most_common(max_words)

    # Format the result
    if not most_common:
        return "No significant words found in the selected posts."

    total_words = sum(count for _, count in most_common)

    result = f"Word Cloud Analysis (top {len(most_common)} words from {total_words} total filtered words):\n\n"

    # Calculate the maximum frequency for scaling
    max_freq = most_common[0][1]

    # Create a visual representation of word frequencies
    for word, count in most_common:
        # Calculate percentage of total
        percentage = (count / total_words) * 100
        # Scale the bar length
        bar_length = int((count / max_freq) * 30)
        bar = "█" * bar_length
        result += f"{word}: {count} ({percentage:.1f}%) {bar}\n"

    return result


@mcp.tool()
def word_cloud_by_post_ids(
    start_id: int, end_id: int, min_word_length: int = 3, max_words: int = 100
) -> str:
    """
    Generate a word cloud analysis showing the most common words used in posts within a specified ID range.

    Args:
        start_id: Starting post ID
        end_id: Ending post ID
        min_word_length: Minimum length of words to include (default: 3)
        max_words: Maximum number of words to return (default: 100)
    """
    if start_id > end_id:
        return "Error: start_id must be less than or equal to end_id."

    # Collect posts within the ID range
    selected_posts = []
    for post in posts:
        post_id = post.get("post_metadata", {}).get("id", 0)
        if start_id <= post_id <= end_id:
            selected_posts.append(post)

    if not selected_posts:
        return f"No posts found with IDs between {start_id} and {end_id}."

    # Extract post texts
    post_texts = [post.get("text", "") for post in selected_posts]

    # Generate word cloud
    cloud = generate_word_cloud(post_texts, min_word_length, max_words)

    # Add additional information
    earliest_id = min(
        post.get("post_metadata", {}).get("id", 0) for post in selected_posts
    )
    latest_id = max(
        post.get("post_metadata", {}).get("id", 0) for post in selected_posts
    )

    earliest_date = min(
        post.get("post_metadata", {}).get("time", 0) for post in selected_posts
    )
    latest_date = max(
        post.get("post_metadata", {}).get("time", 0) for post in selected_posts
    )

    earliest_date_str = (
        datetime.fromtimestamp(earliest_date).strftime("%Y-%m-%d")
        if earliest_date
        else "Unknown"
    )
    latest_date_str = (
        datetime.fromtimestamp(latest_date).strftime("%Y-%m-%d")
        if latest_date
        else "Unknown"
    )

    result = f"Word Cloud Analysis for Post IDs {earliest_id} to {latest_id}\n"
    result += f"Date Range: {earliest_date_str} to {latest_date_str}\n"
    result += f"Total Posts Analyzed: {len(selected_posts)}\n\n"
    result += cloud

    return result


@mcp.tool()
def word_cloud_by_date_range(
    start_date: str, end_date: str, min_word_length: int = 3, max_words: int = 100
) -> str:
    """
    Generate a word cloud analysis showing the most common words used in posts within a specified date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        min_word_length: Minimum length of words to include (default: 3)
        max_words: Maximum number of words to return (default: 100)
    """
    try:
        # Validate date format
        start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        end_timestamp = (
            int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()) + 86400
        )  # Add a day in seconds
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format."

    # Collect posts within the date range
    selected_posts = []
    for post in posts:
        post_time = post.get("post_metadata", {}).get("time", 0)
        if start_timestamp <= post_time <= end_timestamp:
            selected_posts.append(post)

    if not selected_posts:
        return f"No posts found between {start_date} and {end_date}."

    # Extract post texts
    post_texts = [post.get("text", "") for post in selected_posts]

    # Generate word cloud
    cloud = generate_word_cloud(post_texts, min_word_length, max_words)

    # Get post ID range
    earliest_id = min(
        post.get("post_metadata", {}).get("id", 0) for post in selected_posts
    )
    latest_id = max(
        post.get("post_metadata", {}).get("id", 0) for post in selected_posts
    )

    result = f"Word Cloud Analysis for Date Range: {start_date} to {end_date}\n"
    result += f"Post ID Range: {earliest_id} to {latest_id}\n"
    result += f"Total Posts Analyzed: {len(selected_posts)}\n\n"
    result += cloud

    return result


def main():
    if not posts:
        print("Warning: No posts loaded from the dataset.")
    else:
        print(f"Loaded {len(posts)} posts from the dataset.")

    print("Q-Anon Posts MCP Server starting... (Press Ctrl+C to exit)")

    try:
        # Run the MCP server
        mcp.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully - FastMCP will handle cleanup
        print("\nKeyboard interrupt received. Shutting down...")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        print("Q-Anon Posts MCP Server stopped.")


# Run the server
if __name__ == "__main__":
    main()
