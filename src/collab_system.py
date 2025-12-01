#!/usr/bin/env python3
"""Collaborative System: Roles, Discussions, Assignments"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    """Initialize collaboration tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users/Contributors
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'contributor',
        email TEXT,
        active INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )"""
    )

    # Discussions
    c.execute(
        """CREATE TABLE IF NOT EXISTS discussions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        context_type TEXT,
        context_id INTEGER,
        status TEXT DEFAULT 'open',
        created_by TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )"""
    )

    # Comments
    c.execute(
        """CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discussion_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        reply_to INTEGER,
        created_at TEXT NOT NULL,
        FOREIGN KEY (discussion_id) REFERENCES discussions(id),
        FOREIGN KEY (reply_to) REFERENCES comments(id)
    )"""
    )

    # Assignments
    c.execute(
        """CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_type TEXT NOT NULL,
        item_id INTEGER NOT NULL,
        assigned_to TEXT NOT NULL,
        assigned_by TEXT,
        status TEXT DEFAULT 'assigned',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )"""
    )

    # Notifications
    c.execute(
        """CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        type TEXT NOT NULL,
        message TEXT NOT NULL,
        link TEXT,
        read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )"""
    )

    conn.commit()
    conn.close()


# === USERS ===
def add_user(username, role="contributor", email=None):
    """Add user/contributor"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    try:
        c.execute(
            "INSERT INTO users (username, role, email, created_at) VALUES (?, ?, ?, ?)",
            (username, role, email, now),
        )
        conn.commit()
        user_id = c.lastrowid
    except sqlite3.IntegrityError:
        user_id = None
    finally:
        conn.close()
    return user_id


def update_user_role(username, role):
    """Update user role"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET role=? WHERE username=?", (role, username))
    conn.commit()
    conn.close()


def list_users(role=None):
    """List users"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if role:
        c.execute(
            "SELECT * FROM users WHERE role=? AND active=1 ORDER BY username", (role,)
        )
    else:
        c.execute("SELECT * FROM users WHERE active=1 ORDER BY role, username")
    results = c.fetchall()
    conn.close()
    return results


# === DISCUSSIONS ===
def start_discussion(title, created_by, context_type=None, context_id=None):
    """Start a discussion"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        """INSERT INTO discussions (title, context_type, context_id, created_by, created_at, updated_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (title, context_type, context_id, created_by, now, now),
    )
    conn.commit()
    disc_id = c.lastrowid
    conn.close()

    # Notify maintainers
    notify_role(
        "maintainer", "discussion", f"New discussion: {title}", f"discussion:{disc_id}"
    )

    return disc_id


def add_comment(discussion_id, author, content, reply_to=None):
    """Add comment to discussion"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    c.execute(
        """INSERT INTO comments (discussion_id, author, content, reply_to, created_at)
                 VALUES (?, ?, ?, ?, ?)""",
        (discussion_id, author, content, reply_to, now),
    )

    # Update discussion timestamp
    c.execute("UPDATE discussions SET updated_at=? WHERE id=?", (now, discussion_id))

    conn.commit()
    comment_id = c.lastrowid

    # Get discussion participants
    c.execute(
        """SELECT DISTINCT author FROM comments WHERE discussion_id=? AND author!=?""",
        (discussion_id, author),
    )
    participants = [r[0] for r in c.fetchall()]

    # Get discussion creator
    c.execute("SELECT created_by FROM discussions WHERE id=?", (discussion_id,))
    creator = c.fetchone()[0]
    if creator != author and creator not in participants:
        participants.append(creator)

    conn.close()

    # Notify participants
    for user in participants:
        notify_user(
            user,
            "comment",
            f"{author} commented on discussion",
            f"discussion:{discussion_id}",
        )

    return comment_id


def close_discussion(discussion_id, user):
    """Close discussion"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "UPDATE discussions SET status=?, updated_at=? WHERE id=?",
        ("closed", now, discussion_id),
    )
    conn.commit()
    conn.close()


def list_discussions(status=None, context_type=None):
    """List discussions"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if status and context_type:
        c.execute(
            "SELECT * FROM discussions WHERE status=? AND context_type=? ORDER BY updated_at DESC",
            (status, context_type),
        )
    elif status:
        c.execute(
            "SELECT * FROM discussions WHERE status=? ORDER BY updated_at DESC",
            (status,),
        )
    elif context_type:
        c.execute(
            "SELECT * FROM discussions WHERE context_type=? ORDER BY updated_at DESC",
            (context_type,),
        )
    else:
        c.execute("SELECT * FROM discussions ORDER BY updated_at DESC")

    results = c.fetchall()
    conn.close()
    return results


def get_discussion(discussion_id):
    """Get discussion with comments"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM discussions WHERE id=?", (discussion_id,))
    discussion = c.fetchone()

    c.execute(
        "SELECT * FROM comments WHERE discussion_id=? ORDER BY created_at",
        (discussion_id,),
    )
    comments = c.fetchall()

    conn.close()
    return discussion, comments


# === ASSIGNMENTS ===
def assign_item(item_type, item_id, assigned_to, assigned_by):
    """Assign item to user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    c.execute(
        """INSERT INTO assignments (item_type, item_id, assigned_to, assigned_by, created_at, updated_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (item_type, item_id, assigned_to, assigned_by, now, now),
    )

    conn.commit()
    assign_id = c.lastrowid
    conn.close()

    # Notify assignee
    notify_user(
        assigned_to,
        "assignment",
        f"{assigned_by} assigned you {item_type} #{item_id}",
        f"{item_type}:{item_id}",
    )

    return assign_id


def update_assignment(assign_id, status):
    """Update assignment status"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "UPDATE assignments SET status=?, updated_at=? WHERE id=?",
        (status, now, assign_id),
    )
    conn.commit()
    conn.close()


def list_assignments(user=None, status=None):
    """List assignments"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if user and status:
        c.execute(
            "SELECT * FROM assignments WHERE assigned_to=? AND status=? ORDER BY created_at DESC",
            (user, status),
        )
    elif user:
        c.execute(
            "SELECT * FROM assignments WHERE assigned_to=? ORDER BY status, created_at DESC",
            (user,),
        )
    elif status:
        c.execute(
            "SELECT * FROM assignments WHERE status=? ORDER BY created_at DESC",
            (status,),
        )
    else:
        c.execute("SELECT * FROM assignments ORDER BY status, created_at DESC")

    results = c.fetchall()
    conn.close()
    return results


# === NOTIFICATIONS ===
def notify_user(user, type, message, link=None):
    """Send notification to user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "INSERT INTO notifications (user, type, message, link, created_at) VALUES (?, ?, ?, ?, ?)",
        (user, type, message, link, now),
    )
    conn.commit()
    conn.close()


def notify_role(role, type, message, link=None):
    """Send notification to all users with role"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE role=? AND active=1", (role,))
    users = [r[0] for r in c.fetchall()]
    conn.close()

    for user in users:
        notify_user(user, type, message, link)


def get_notifications(user, unread_only=False):
    """Get user notifications"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if unread_only:
        c.execute(
            "SELECT * FROM notifications WHERE user=? AND read=0 ORDER BY created_at DESC",
            (user,),
        )
    else:
        c.execute(
            "SELECT * FROM notifications WHERE user=? ORDER BY created_at DESC LIMIT 50",
            (user,),
        )

    results = c.fetchall()
    conn.close()
    return results


def mark_read(notification_id):
    """Mark notification as read"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE notifications SET read=1 WHERE id=?", (notification_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Users:       python collab_system.py user <add|list|role> ...")
        print(
            "  Discussions: python collab_system.py discuss <start|comment|list|show|close> ..."
        )
        print("  Assignments: python collab_system.py assign <create|list|update> ...")
        print("  Notify:      python collab_system.py notify <user> ...")
        sys.exit(1)

    module = sys.argv[1]
    cmd = sys.argv[2] if len(sys.argv) > 2 else None

    # === USER COMMANDS ===
    if module == "user":
        if cmd == "add" and len(sys.argv) >= 5:
            user_id = add_user(sys.argv[3], sys.argv[4])
            print(f"Added user: {sys.argv[3]} ({sys.argv[4]})")

        elif cmd == "role" and len(sys.argv) >= 5:
            update_user_role(sys.argv[3], sys.argv[4])
            print(f"Updated {sys.argv[3]} role to {sys.argv[4]}")

        elif cmd == "list":
            role = sys.argv[3] if len(sys.argv) > 3 else None
            users = list_users(role)
            for u in users:
                print(f"{u[1]} ({u[2]})")

    # === DISCUSSION COMMANDS ===
    elif module == "discuss":
        if cmd == "start" and len(sys.argv) >= 5:
            disc_id = start_discussion(sys.argv[3], sys.argv[4])
            print(f"Started discussion #{disc_id}")

        elif cmd == "comment" and len(sys.argv) >= 5:
            comment_id = add_comment(int(sys.argv[3]), sys.argv[4], sys.argv[5])
            print(f"Added comment #{comment_id}")

        elif cmd == "show" and len(sys.argv) >= 4:
            disc, comments = get_discussion(int(sys.argv[3]))
            print(f"\n{disc[1]} (by {disc[5]})")
            print("=" * 60)
            for c in comments:
                print(f"\n[{c[2]}] {c[3]}")

        elif cmd == "close" and len(sys.argv) >= 4:
            close_discussion(int(sys.argv[3]), sys.argv[4])
            print(f"Closed discussion #{sys.argv[3]}")

        elif cmd == "list":
            status = sys.argv[3] if len(sys.argv) > 3 else None
            discussions = list_discussions(status)
            for d in discussions:
                print(f"[{d[4]}] #{d[0]}: {d[1]} (by {d[5]})")

    # === ASSIGNMENT COMMANDS ===
    elif module == "assign":
        if cmd == "create" and len(sys.argv) >= 6:
            assign_id = assign_item(
                sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6]
            )
            print(f"Assigned {sys.argv[3]} #{sys.argv[4]} to {sys.argv[5]}")

        elif cmd == "list":
            user = sys.argv[3] if len(sys.argv) > 3 else None
            assignments = list_assignments(user)
            for a in assignments:
                print(f"[{a[6]}] {a[1]} #{a[2]} → {a[3]}")

        elif cmd == "update" and len(sys.argv) >= 5:
            update_assignment(int(sys.argv[3]), sys.argv[4])
            print(f"Updated assignment #{sys.argv[3]}")

    # === NOTIFICATION COMMANDS ===
    elif module == "notify":
        if len(sys.argv) >= 3:
            notifications = get_notifications(sys.argv[2], unread_only=True)
            print(f"\nNotifications for {sys.argv[2]} ({len(notifications)} unread):")
            for n in notifications:
                print(f"  [{n[2]}] {n[3]}")
