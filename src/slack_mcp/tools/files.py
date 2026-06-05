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
    """Delete an existing comment on a file."""
    return await client.api_call("files.comments.delete", file=file, id=id)


@mcp.tool
async def files_complete_upload_external(
    files: list[dict[str, str]],
    channel_id: str | None = None,
    initial_comment: str | None = None,
    thread_ts: str | None = None,
    client: SlackClient = Depends(slack_client),
) -> dict:
    """Complete an upload external process."""
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
    return await client.api_call(
        "files.getUploadURLExternal",
        filename=filename,
        length=length,
        alt_txt=alt_txt,
        snippet_type=snippet_type,
    )


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
    """Get information about a file. Set detailed=True for full response."""
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
    """List files for a team, channel, or user. Set detailed=True for full response."""
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
    """Add a remote file."""
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
    """Get information about a remote file."""
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
    """List remote files."""
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
    """Remove a remote file."""
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
    """Share a remote file into a channel."""
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
    """Update a remote file."""
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
    return await client.api_call(
        "files.upload.v2",
        channel_id=channel_id,
        content=content,
        filename=filename,
        filetype=filetype,
        initial_comment=initial_comment,
        length=length,
        snippet_type=snippet_type,
        thread_ts=thread_ts,
        title=title,
    )
