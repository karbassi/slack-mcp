from fastmcp.dependencies import Depends

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp, slack_client


@mcp.tool
async def files_comments_delete(
    file: str,
    id: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete an existing comment on a file."""
    return await client.api_call("files.comments.delete", file=file, id=id)


@mcp.tool
async def files_complete_upload_external(
    files: list,
    channel_id: str | None = None,
    initial_comment: str | None = None,
    thread_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Complete an upload external process."""
    kwargs = {"files": files}
    if channel_id is not None:
        kwargs["channel_id"] = channel_id
    if initial_comment is not None:
        kwargs["initial_comment"] = initial_comment
    if thread_ts is not None:
        kwargs["thread_ts"] = thread_ts
    return await client.api_call_json("files.completeUploadExternal", **kwargs)


@mcp.tool
async def files_delete(
    file: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Delete a file."""
    return await client.api_call("files.delete", file=file)


@mcp.tool
async def files_get_upload_url_external(
    filename: str,
    length: int,
    alt_txt: str | None = None,
    snippet_type: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get an upload URL for an external file."""
    kwargs = {"filename": filename, "length": length}
    if alt_txt is not None:
        kwargs["alt_txt"] = alt_txt
    if snippet_type is not None:
        kwargs["snippet_type"] = snippet_type
    return await client.api_call("files.getUploadURLExternal", **kwargs)


@mcp.tool
async def files_info(
    file: str,
    count: int | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    page: int | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a file."""
    kwargs = {"file": file}
    if count is not None:
        kwargs["count"] = count
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if page is not None:
        kwargs["page"] = page
    return await client.api_call("files.info", **kwargs)


@mcp.tool
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
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List files for a team, channel, or user."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if count is not None:
        kwargs["count"] = count
    if page is not None:
        kwargs["page"] = page
    if show_files_hidden_by_limit is not None:
        kwargs["show_files_hidden_by_limit"] = show_files_hidden_by_limit
    if team_id is not None:
        kwargs["team_id"] = team_id
    if ts_from is not None:
        kwargs["ts_from"] = ts_from
    if ts_to is not None:
        kwargs["ts_to"] = ts_to
    if types is not None:
        kwargs["types"] = types
    if user is not None:
        kwargs["user"] = user
    return await client.api_call("files.list", **kwargs)


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
    """Add a remote file."""
    kwargs = {
        "external_id": external_id,
        "external_url": external_url,
        "title": title,
    }
    if filetype is not None:
        kwargs["filetype"] = filetype
    if indexable_file_contents is not None:
        kwargs["indexable_file_contents"] = indexable_file_contents
    if preview_image is not None:
        kwargs["preview_image"] = preview_image
    return await client.api_call("files.remote.add", **kwargs)


@mcp.tool
async def files_remote_info(
    external_id: str | None = None,
    file: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Get information about a remote file."""
    kwargs = {}
    if external_id is not None:
        kwargs["external_id"] = external_id
    if file is not None:
        kwargs["file"] = file
    return await client.api_call("files.remote.info", **kwargs)


@mcp.tool
async def files_remote_list(
    channel: str | None = None,
    cursor: str | None = None,
    limit: int | None = None,
    ts_from: str | None = None,
    ts_to: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """List remote files."""
    kwargs = {}
    if channel is not None:
        kwargs["channel"] = channel
    if cursor is not None:
        kwargs["cursor"] = cursor
    if limit is not None:
        kwargs["limit"] = limit
    if ts_from is not None:
        kwargs["ts_from"] = ts_from
    if ts_to is not None:
        kwargs["ts_to"] = ts_to
    return await client.api_call("files.remote.list", **kwargs)


@mcp.tool
async def files_remote_remove(
    external_id: str | None = None,
    file: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Remove a remote file."""
    kwargs = {}
    if external_id is not None:
        kwargs["external_id"] = external_id
    if file is not None:
        kwargs["file"] = file
    return await client.api_call("files.remote.remove", **kwargs)


@mcp.tool
async def files_remote_share(
    channels: str,
    external_id: str | None = None,
    file: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Share a remote file into a channel."""
    kwargs = {"channels": channels}
    if external_id is not None:
        kwargs["external_id"] = external_id
    if file is not None:
        kwargs["file"] = file
    return await client.api_call("files.remote.share", **kwargs)


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
    """Update a remote file."""
    kwargs = {}
    if external_id is not None:
        kwargs["external_id"] = external_id
    if external_url is not None:
        kwargs["external_url"] = external_url
    if file is not None:
        kwargs["file"] = file
    if filetype is not None:
        kwargs["filetype"] = filetype
    if indexable_file_contents is not None:
        kwargs["indexable_file_contents"] = indexable_file_contents
    if preview_image is not None:
        kwargs["preview_image"] = preview_image
    if title is not None:
        kwargs["title"] = title
    return await client.api_call("files.remote.update", **kwargs)


@mcp.tool
async def files_revoke_public_url(
    file: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Revoke public/external sharing access for a file."""
    return await client.api_call("files.revokePublicURL", file=file)


@mcp.tool
async def files_shared_public_url(
    file: str,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Enable a file for public/external sharing."""
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
    """Upload a file (legacy)."""
    kwargs = {}
    if channels is not None:
        kwargs["channels"] = channels
    if content is not None:
        kwargs["content"] = content
    if filename is not None:
        kwargs["filename"] = filename
    if filetype is not None:
        kwargs["filetype"] = filetype
    if initial_comment is not None:
        kwargs["initial_comment"] = initial_comment
    if thread_ts is not None:
        kwargs["thread_ts"] = thread_ts
    if title is not None:
        kwargs["title"] = title
    return await client.api_call("files.upload", **kwargs)


@mcp.tool
async def files_upload_v2(
    channel_id: str | None = None,
    content: str | None = None,
    filename: str | None = None,
    filetype: str | None = None,
    initial_comment: str | None = None,
    length: int | None = None,
    snippet_type: str | None = None,
    thread_ts: str | None = None,
    title: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Upload a file using v2 API."""
    kwargs = {}
    if channel_id is not None:
        kwargs["channel_id"] = channel_id
    if content is not None:
        kwargs["content"] = content
    if filename is not None:
        kwargs["filename"] = filename
    if filetype is not None:
        kwargs["filetype"] = filetype
    if initial_comment is not None:
        kwargs["initial_comment"] = initial_comment
    if length is not None:
        kwargs["length"] = length
    if snippet_type is not None:
        kwargs["snippet_type"] = snippet_type
    if thread_ts is not None:
        kwargs["thread_ts"] = thread_ts
    if title is not None:
        kwargs["title"] = title
    return await client.api_call("files.upload.v2", **kwargs)
