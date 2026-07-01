from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.compact import compact_file_list, compactable
from slack_mcp.server import SHORT_TTL, mcp, slack_client


@mcp.tool
async def files_comments_delete(
    file: str,
    id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete an existing comment on a file.

    Args:
        file: ID of the file the comment belongs to (e.g. ``F0123``).
        id: ID of the comment to delete.
    """
    return await client.api_call("files.comments.delete", file=file, id=id)


@mcp.tool
async def files_complete_upload_external(
    files: list[dict[str, str]],
    channel_id: str | None = None,
    initial_comment: str | None = None,
    thread_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Complete an upload external process.

    Args:
        files: File objects to finalize, each with an ``id`` from ``files.getUploadURLExternal`` and optional ``title``.
        channel_id: ID of the channel to share the uploaded files into (e.g. ``C0123``).
        initial_comment: Message text to post alongside the shared files.
        thread_ts: Timestamp of the parent message to share the files into as a thread reply (e.g. ``1700000000.00``).
    """
    return await client.api_call_json(
        "files.completeUploadExternal",
        files=files,
        channel_id=channel_id,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
    )


@mcp.tool
async def files_delete(
    file: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a file.

    Args:
        file: ID of the file to delete (e.g. ``F0123``).
    """
    return await client.api_call("files.delete", file=file)


@mcp.tool
async def files_get_upload_url_external(
    filename: str,
    length: int,
    alt_txt: str | None = None,
    snippet_type: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get an upload URL for an external file.

    Args:
        filename: Name of the file being uploaded (e.g. ``report.pdf``).
        length: Size of the file in bytes.
        alt_txt: Description of the image for screen-reader accessibility.
        snippet_type: Syntax type of a snippet being uploaded (e.g. ``python``).
    """
    return await client.api_call(
        "files.getUploadURLExternal",
        filename=filename,
        length=length,
        alt_txt=alt_txt,
        snippet_type=snippet_type,
    )


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def files_favorites_list(
    type: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List a user's favorited (starred/saved) files (undocumented).

    Args:
        type: File category to list favorites for (e.g. ``all``, ``images``,
            ``pdfs``, ``snippets``, ``gdocs``, ``spaces``).
    """
    return await client.session_call("files.favorites.list", type=type)


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
async def files_get_shares(
    file_id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get where a file has been shared (undocumented).

    Args:
        file_id: ID of the file to look up shares for (e.g. ``F0123``).
    """
    return await client.session_call("files.getShares", file_id=file_id)


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
@compactable(compact_file_list)
async def files_recently_deleted(
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List recently deleted files that can still be recovered (undocumented).

    Set detailed=True for the full response.

    Args:
        detailed: Return the full Slack response instead of the compacted summary when ``True``.
    """
    return await client.session_call("files.recentlyDeleted")


@mcp.tool(meta={"cache_ttl": SHORT_TTL})
@compactable(compact_file_list)
async def files_info(
    file: str,
    count: int | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    page: int | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a file. Set detailed=True for full response.

    Args:
        file: ID of the file to get info about (e.g. ``F0123``).
        count: Number of comments to return per page (deprecated pagination).
        cursor: Pagination cursor from a prior response's ``response_metadata.next_cursor``.
        limit: Maximum number of comments to return per page.
        page: Page number of comments to return (deprecated pagination).
        detailed: Return the full Slack response instead of the compacted summary when ``True``.
    """
    return await client.api_call(
        "files.info", file=file, count=count, cursor=cursor, limit=limit, page=page
    )


@mcp.tool
@compactable(compact_file_list)
async def files_list(
    channel: str | None = None,
    count: int | None = None,
    page: int | None = None,
    show_files_hidden_by_limit: bool | None = None,
    team_id: str | None = None,
    ts_from: str | None = None,
    ts_to: str | None = None,
    types: str | None = None,
    user: str | None = None,
    detailed: bool = False,  # noqa: ARG001
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List files for a team, channel, or user. Set detailed=True for full response.

    Args:
        channel: Filter files to those shared in this channel (e.g. ``C0123``).
        count: Number of files to return per page.
        page: Page number of results to return.
        show_files_hidden_by_limit: Include files hidden due to the free-plan message/file limit when ``True``.
        team_id: ID of the workspace to list files for, required for org-wide tokens (e.g. ``T0123``).
        ts_from: Filter files created after this Unix timestamp.
        ts_to: Filter files created before this Unix timestamp.
        types: Comma-separated file types to filter by (e.g. ``images,pdfs``; also ``all``, ``snippets``, ``gdocs``).
        user: Filter files to those created by this user (e.g. ``U0123``).
        detailed: Return the full Slack response instead of the compacted summary when ``True``.
    """
    return await client.api_call(
        "files.list",
        channel=channel,
        count=count,
        page=page,
        show_files_hidden_by_limit=show_files_hidden_by_limit,
        team_id=team_id,
        ts_from=ts_from,
        ts_to=ts_to,
        types=types,
        user=user,
    )


@mcp.tool
async def files_remote_add(
    external_id: str,
    external_url: str,
    title: str,
    filetype: str | None = None,
    indexable_file_contents: str | None = None,
    preview_image: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Add a remote file.

    Args:
        external_id: Unique identifier for the file in your app's storage (e.g. ``123abc``).
        external_url: URL where the remote file can be accessed (e.g. ``https://example.com/files/123``).
        title: Title of the file shown in Slack.
        filetype: File type identifier (e.g. ``doc``, ``pdf``).
        indexable_file_contents: Plain-text contents of the file used to make it searchable in Slack.
        preview_image: Image to use as the file's preview thumbnail.
    """
    return await client.api_call(
        "files.remote.add",
        external_id=external_id,
        external_url=external_url,
        title=title,
        filetype=filetype,
        indexable_file_contents=indexable_file_contents,
        preview_image=preview_image,
    )


@mcp.tool
async def files_remote_info(
    external_id: str | None = None,
    file: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a remote file.

    Args:
        external_id: Identifier of the remote file in your app's storage (e.g. ``123abc``).
        file: ID of the file as assigned by Slack (e.g. ``F0123``).
    """
    return await client.api_call(
        "files.remote.info", external_id=external_id, file=file
    )


@mcp.tool
async def files_remote_list(
    channel: str | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    ts_from: str | None = None,
    ts_to: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List remote files.

    Args:
        channel: Filter to remote files shared in this channel (e.g. ``C0123``).
        cursor: Pagination cursor for the next page, from a prior response's ``response_metadata.next_cursor``.
        limit: Maximum number of files to return per page.
        ts_from: Filter files created after this Unix timestamp.
        ts_to: Filter files created before this Unix timestamp.
    """
    return await client.api_call(
        "files.remote.list",
        channel=channel,
        cursor=cursor,
        limit=limit,
        ts_from=ts_from,
        ts_to=ts_to,
    )


@mcp.tool
async def files_remote_remove(
    external_id: str | None = None,
    file: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a remote file.

    Args:
        external_id: Identifier of the remote file in your app's storage (e.g. ``123abc``).
        file: ID of the file as assigned by Slack (e.g. ``F0123``).
    """
    return await client.api_call(
        "files.remote.remove", external_id=external_id, file=file
    )


@mcp.tool
async def files_remote_share(
    channels: str,
    external_id: str | None = None,
    file: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Share a remote file into a channel.

    Args:
        channels: Comma-separated list of channel IDs to share the file into (e.g. ``C0123,C0456``).
        external_id: Identifier of the remote file in your app's storage (e.g. ``123abc``).
        file: ID of the file as assigned by Slack (e.g. ``F0123``).
    """
    return await client.api_call(
        "files.remote.share", channels=channels, external_id=external_id, file=file
    )


@mcp.tool
async def files_remote_update(
    external_id: str | None = None,
    external_url: str | None = None,
    file: str | None = None,
    filetype: str | None = None,
    indexable_file_contents: str | None = None,
    preview_image: str | None = None,
    title: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Update a remote file.

    Args:
        external_id: Identifier of the remote file in your app's storage (e.g. ``123abc``).
        external_url: URL where the remote file can be accessed (e.g. ``https://example.com/files/123``).
        file: ID of the file as assigned by Slack (e.g. ``F0123``).
        filetype: File type identifier (e.g. ``doc``, ``pdf``).
        indexable_file_contents: Plain-text contents of the file used to make it searchable in Slack.
        preview_image: Image to use as the file's preview thumbnail.
        title: Title of the file shown in Slack.
    """
    return await client.api_call(
        "files.remote.update",
        external_id=external_id,
        external_url=external_url,
        file=file,
        filetype=filetype,
        indexable_file_contents=indexable_file_contents,
        preview_image=preview_image,
        title=title,
    )


@mcp.tool
async def files_revoke_public_url(
    file: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Revoke public/external sharing access for a file.

    Args:
        file: ID of the file to revoke public sharing for (e.g. ``F0123``).
    """
    return await client.api_call("files.revokePublicURL", file=file)


@mcp.tool
async def files_shared_public_url(
    file: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Enable a file for public/external sharing.

    Args:
        file: ID of the file to enable public sharing for (e.g. ``F0123``).
    """
    return await client.api_call("files.sharedPublicURL", file=file)


@mcp.tool
async def files_upload(
    channels: str | None = None,
    content: str | None = None,
    filename: str | None = None,
    filetype: str | None = None,
    initial_comment: str | None = None,
    thread_ts: str | None = None,
    title: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Upload a file (legacy).

    Args:
        channels: Comma-separated list of channel IDs to share the file into (e.g. ``C0123,C0456``).
        content: File contents as a string; using this creates an editable text/snippet file instead of a binary upload.
        filename: Name of the file (e.g. ``report.pdf``).
        filetype: File type identifier (e.g. ``python``, ``pdf``).
        initial_comment: Message text to post alongside the file.
        thread_ts: Timestamp of the parent message to share the file into as a thread reply (e.g. ``1700000000.00``).
        title: Title of the file shown in Slack.
    """
    return await client.api_call(
        "files.upload",
        channels=channels,
        content=content,
        filename=filename,
        filetype=filetype,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
        title=title,
    )


@mcp.tool
async def files_upload_v2(
    content: str,
    filename: str | None = None,
    title: str | None = None,
    channel: str | None = None,
    initial_comment: str | None = None,
    thread_ts: str | None = None,
    snippet_type: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Upload file content (v2).

    Runs Slack's recommended upload flow (get upload URL, upload, complete) via
    the slack_sdk helper. Takes the file contents directly — it does not read
    from the host filesystem.

    Args:
        content: File contents to upload as a string.
        filename: Name of the file (e.g. ``notes.txt``).
        title: Title of the file shown in Slack.
        channel: ID of the channel to share the uploaded file into (e.g. ``C0123``).
        initial_comment: Message text to post alongside the file.
        thread_ts: Timestamp of the parent message to share the file into as a thread reply (e.g. ``1700000000.0001``).
        snippet_type: Syntax type of a snippet being uploaded (e.g. ``python``).
    """
    return await client.files_upload_v2(
        content=content,
        filename=filename,
        title=title,
        channel=channel,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
        snippet_type=snippet_type,
    )
