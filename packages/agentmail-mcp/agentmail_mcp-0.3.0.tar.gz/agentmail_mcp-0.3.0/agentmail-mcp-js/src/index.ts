import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const AGENTMAIL_URL_BASE = "https://api.agentmail.to/v0";

// Create server instance
const server = new McpServer({
  name: "agentmail",
  version: "1.0.0",
  capabilities: {
    resources: {},
    tools: {},
  },
});

// Define interfaces for API responses
interface Inbox {
  inbox_id: string;
  organization_id: string;
  created_at: string;
  display_name?: string;
}

// Define a ThreadMessage interface for messages in a thread
interface ThreadMessage {
  thread_id: string;
  message_id: string;
  event_id: string;
  labels: string[];
  timestamp: string;
  from: string;
  to: string[];
  inbox_id: string;
  organization_id: string;
  text: string;
}

// Update the Thread interface
interface Thread {
  thread_id: string;
  event_id: string;
  labels: string[];
  timestamp: string;
  senders: string[];
  recipients: string[];
  message_count: number;
  messages: ThreadMessage[];
  inbox_id: string;
  organization_id: string;
  subject: string;
  preview: string;
}

// Update the Message interface to match the API response
interface Message {
  thread_id: string;
  message_id: string;
  event_id: string;
  labels: string[];
  timestamp: string;
  from: string;
  to: string[];
  cc?: string[];
  bcc?: string[];
  subject: string;
  preview: string;
  inbox_id: string;
  organization_id: string;
  reply_to?: string;
  text: string;
  html?: string;
  in_reply_to?: string;
  references?: string[];
  attachments?: Array<{
    attachment_id: string;
    filename: string;
    content_type: string;
    size: number;
    inline: boolean;
  }>;
}

interface Attachment {
  attachment_id: string;
  message_id: string;
  filename: string;
  content_type: string;
  size: number;
  url: string;
  inline: boolean;
}

// Helper function for making AgentMail API requests
async function makeAgentMailRequest<T>(
  method: string,
  path: string,
  apiKey: string,
  data?: any,
  params?: Record<string, any>
): Promise<T | null> {
  const url = new URL(`${AGENTMAIL_URL_BASE}${path}`);

  // Add query parameters if provided
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        url.searchParams.append(key, value.toString());
      }
    });
  }

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
  };

  try {
    console.error(`Making ${method} request to ${url.toString()}`);

    const options: RequestInit = {
      method: method.toUpperCase(),
      headers: headers,
    };

    if (
      data &&
      (method.toUpperCase() === "POST" || method.toUpperCase() === "PUT")
    ) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url.toString(), options);

    console.error(`Response status: ${response.status}`);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`
      );
    }

    const responseData = await response.json();
    console.error(`Response data:`, responseData);
    return responseData as T;
  } catch (error) {
    console.error(`Error making AgentMail request (${method} ${path}):`, error);
    return null;
  }
}

// Get API key from command line arguments
const apiKeyIndex = process.argv.findIndex((arg) => arg === "--api-key");
const apiKey =
  apiKeyIndex >= 0 && apiKeyIndex < process.argv.length - 1
    ? process.argv[apiKeyIndex + 1]
    : null;

if (!apiKey) {
  console.error("Error: --api-key is required");
  process.exit(1);
}

// Register inbox tools
server.tool(
  "listInboxes",
  "List all inboxes. Use this tool when the user asks to see their available email inboxes, view all email addresses, check what inboxes exist, or get a list of their email accounts.",
  {
    limit: z
      .number()
      .optional()
      .describe("Maximum number of inboxes to return"),
    last_key: z.string().optional().describe("Key of last item for pagination"),
  },
  async ({ limit, last_key }) => {
    const params: Record<string, any> = {};
    if (limit !== undefined) params.limit = limit;
    if (last_key !== undefined) params.last_key = last_key;

    const result = await makeAgentMailRequest<{
      inboxes: Inbox[];
      count: number;
      limit?: number;
      last_key?: string;
    }>("GET", "/inboxes", apiKey, undefined, params);

    if (!result) {
      return {
        content: [{ type: "text", text: "Failed to retrieve inboxes" }],
      };
    }

    if (!result.inboxes || result.inboxes.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: "No inboxes found. You may need to create an inbox first.",
          },
        ],
      };
    }

    const inboxesText = `Found ${result.inboxes.length} inboxes (total count: ${
      result.count
    }):\n\n${result.inboxes
      .map(
        (inbox) =>
          `ID: ${inbox.inbox_id}\nEmail: ${inbox.inbox_id}\nName: ${
            inbox.display_name || "N/A"
          }\n---`
      )
      .join("\n")}`;

    return {
      content: [{ type: "text", text: inboxesText }],
    };
  }
);

server.tool(
  "getInbox",
  "Get details of a specific inbox by ID. Use this tool when the user asks for information about a particular email inbox, wants to check the details of a specific email address, or needs to verify an inbox exists.",
  {
    inbox_id: z.string().describe("ID of the inbox to retrieve"),
  },
  async ({ inbox_id }) => {
    const result = await makeAgentMailRequest<Inbox>(
      "GET",
      `/inboxes/${inbox_id}`,
      apiKey
    );

    if (!result) {
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve inbox with ID: ${inbox_id}`,
          },
        ],
      };
    }

    const inboxText = `Inbox Details:\nID: ${result.inbox_id}\nEmail: ${
      result.inbox_id
    }\nName: ${result.display_name || "N/A"}\nCreated: ${result.created_at}`;

    return {
      content: [{ type: "text", text: inboxText }],
    };
  }
);

server.tool(
  "createInbox",
  "Create a new email inbox. Use this tool when the user asks to create a new email account, set up a new email address, or generate a new inbox for receiving emails.",
  {
    username: z.string().optional().describe("Email username (optional)"),
    domain: z.string().optional().describe("Email domain (optional)"),
    display_name: z
      .string()
      .optional()
      .describe("Display name for the inbox (optional)"),
  },
  async ({ username, domain, display_name }) => {
    const payload: Record<string, any> = {};
    if (username !== undefined) payload.username = username;
    if (domain !== undefined) payload.domain = domain;
    if (display_name !== undefined) payload.display_name = display_name;

    const result = await makeAgentMailRequest<Inbox>(
      "POST",
      "/inboxes",
      apiKey,
      payload
    );

    if (!result) {
      return {
        content: [{ type: "text", text: "Failed to create inbox" }],
      };
    }

    const inboxText = `Inbox Created Successfully:\nID: ${
      result.inbox_id
    }\nEmail: ${result.inbox_id}\nName: ${result.display_name || "N/A"}`;

    return {
      content: [{ type: "text", text: inboxText }],
    };
  }
);

// Thread tools
server.tool(
  "listThreads",
  "List email conversation threads in an inbox. Use this tool when the user asks to see their email conversations, view email threads, check what emails they've received, or get an overview of messages grouped by conversation.",
  {
    inbox_id: z.string().describe("ID of the inbox"),
    limit: z
      .number()
      .optional()
      .describe("Maximum number of threads to return"),
    last_key: z.string().optional().describe("Key of last item for pagination"),
    received: z.boolean().optional().describe("Filter by received threads"),
    sent: z.boolean().optional().describe("Filter by sent threads"),
  },
  async ({ inbox_id, limit, last_key, received, sent }) => {
    const params: Record<string, any> = {};
    if (limit !== undefined) params.limit = limit;
    if (last_key !== undefined) params.last_key = last_key;
    if (received !== undefined) params.received = received;
    if (sent !== undefined) params.sent = sent;

    const result = await makeAgentMailRequest<{
      threads: Thread[];
      count: number;
      limit: number;
      last_key: string;
    }>("GET", `/inboxes/${inbox_id}/threads`, apiKey, undefined, params);

    if (!result) {
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve threads for inbox: ${inbox_id}`,
          },
        ],
      };
    }

    if (!result.threads || result.threads.length === 0) {
      return {
        content: [{ type: "text", text: "No threads found for this inbox." }],
      };
    }

    const threadsText = `Found ${
      result.threads.length
    } threads:\n\n${result.threads
      .map(
        (thread) =>
          `ID: ${thread.thread_id}\nSubject: ${thread.subject}\nDate: ${thread.timestamp}\nPreview: ${thread.preview}\n---`
      )
      .join("\n")}`;

    return {
      content: [{ type: "text", text: threadsText }],
    };
  }
);

// Update the getThread function
server.tool(
  "getThread",
  "Get a complete email conversation thread. Use this tool when the user asks to see a specific email conversation, view all messages in a thread, or read an entire email exchange.",
  {
    inbox_id: z.string().describe("ID of the inbox"),
    thread_id: z.string().describe("ID of the thread to retrieve"),
  },
  async ({ inbox_id, thread_id }) => {
    const result = await makeAgentMailRequest<Thread>(
      "GET",
      `/inboxes/${inbox_id}/threads/${thread_id}`,
      apiKey
    );

    if (!result) {
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve thread with ID: ${thread_id}`,
          },
        ],
      };
    }

    // Create a more detailed response that includes message info
    const messagesSummary =
      result.messages && result.messages.length > 0
        ? `\n\nMessages (${result.messages.length}):\n${result.messages
            .map(
              (msg, idx) =>
                `${idx + 1}. From: ${msg.from}\n   Date: ${
                  msg.timestamp
                }\n   Preview: ${msg.text.substring(0, 50)}${
                  msg.text.length > 50 ? "..." : ""
                }`
            )
            .join("\n\n")}`
        : "";

    const threadText = `Thread Details:
ID: ${result.thread_id}
Subject: ${result.subject}
Inbox ID: ${result.inbox_id}
Date: ${result.timestamp}
Senders: ${result.senders.join(", ")}
Recipients: ${result.recipients.join(", ")}
Labels: ${result.labels.join(", ")}
Message Count: ${result.message_count}${messagesSummary}`;

    return {
      content: [{ type: "text", text: threadText }],
    };
  }
);

// Message tools
// Update the listMessages tool
server.tool(
  "listMessages",
  "List individual email messages in an inbox. Use this tool when the user asks to see all their emails, view message details, get a flat list of emails (not grouped by conversation), or check what emails they've received.",
  {
    inbox_id: z.string().describe("ID of the inbox"),
    limit: z
      .number()
      .optional()
      .describe("Maximum number of messages to return"),
    last_key: z.string().optional().describe("Key of last item for pagination"),
  },
  async ({ inbox_id, limit, last_key }) => {
    const params: Record<string, any> = {};
    if (limit !== undefined) params.limit = limit;
    if (last_key !== undefined) params.last_key = last_key;

    const result = await makeAgentMailRequest<{
      messages: Message[];
      count: number;
      limit: number;
      last_key: string;
    }>("GET", `/inboxes/${inbox_id}/messages`, apiKey, undefined, params);

    if (!result) {
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve messages for inbox: ${inbox_id}`,
          },
        ],
      };
    }

    if (!result.messages || result.messages.length === 0) {
      return {
        content: [{ type: "text", text: "No messages found for this inbox." }],
      };
    }

    const messagesText = `Found ${
      result.messages.length
    } messages:\n\n${result.messages
      .map(
        (message) =>
          `ID: ${message.message_id}\nSubject: ${message.subject}\nFrom: ${
            message.from
          }\nTo: ${message.to.join(", ")}\nDate: ${message.timestamp}${
            message.attachments && message.attachments.length > 0
              ? `\nAttachments: ${message.attachments.length}`
              : ""
          }\n---`
      )
      .join("\n")}`;

    return {
      content: [{ type: "text", text: messagesText }],
    };
  }
);

// Add getMessage tool
server.tool(
  "getMessage",
  "Get a specific email message by ID. Use this tool when the user asks to read a particular email, view the contents of a specific message, or get details about an individual email.",
  {
    inbox_id: z.string().describe("ID of the inbox"),
    message_id: z.string().describe("ID of the message to retrieve"),
  },
  async ({ inbox_id, message_id }) => {
    const result = await makeAgentMailRequest<Message>(
      "GET",
      `/inboxes/${inbox_id}/messages/${message_id}`,
      apiKey
    );

    if (!result) {
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve message with ID: ${message_id}`,
          },
        ],
      };
    }

    // Build attachment details if present
    const attachmentDetails =
      result.attachments && result.attachments.length > 0
        ? `\n\nAttachments (${result.attachments.length}):\n${result.attachments
            .map(
              (att) =>
                `- ${att.filename} (${att.content_type}, ${att.size} bytes)`
            )
            .join("\n")}`
        : "";

    // Add reply information if present
    const replyInfo = result.in_reply_to
      ? `\nIn Reply To: ${result.in_reply_to}`
      : "";

    // Add references if present
    const referencesInfo =
      result.references && result.references.length > 0
        ? `\nReferences: ${result.references.join(", ")}`
        : "";

    const messageText = `Message Details:
ID: ${result.message_id}
Thread ID: ${result.thread_id}
Subject: ${result.subject}
From: ${result.from}${result.reply_to ? ` (Reply-To: ${result.reply_to})` : ""}
To: ${result.to.join(", ")}
${result.cc ? `CC: ${result.cc.join(", ")}\n` : ""}${
      result.bcc ? `BCC: ${result.bcc.join(", ")}\n` : ""
    }
Date: ${result.timestamp}
Labels: ${result.labels.join(", ")}${replyInfo}${referencesInfo}

Content:
${result.text || result.preview}${attachmentDetails}`;

    return {
      content: [{ type: "text", text: messageText }],
    };
  }
);

server.tool(
  "sendMessage",
  "Send a new email message. Use this tool when the user asks to send an email, compose a new message, write to someone, or initiate a new email conversation.",
  {
    inbox_id: z.string().describe("ID of the sending inbox"),
    to: z
      .union([z.string(), z.array(z.string())])
      .describe("Recipient email address(es)"),
    subject: z.string().optional().describe("Email subject"),
    text: z.string().optional().describe("Email body content"),
    cc: z
      .union([z.string(), z.array(z.string())])
      .optional()
      .describe("CC recipient(s)"),
    bcc: z
      .union([z.string(), z.array(z.string())])
      .optional()
      .describe("BCC recipient(s)"),
    html: z.string().optional().describe("HTML email body"),
  },
  async ({ inbox_id, to, subject, text, cc, bcc, html }) => {
    // Convert single string to array if needed
    const toArray = Array.isArray(to) ? to : [to];

    const payload: Record<string, any> = {
      to: toArray,
    };

    if (subject !== undefined) payload.subject = subject;
    if (text !== undefined) payload.text = text;
    if (cc !== undefined) payload.cc = Array.isArray(cc) ? cc : [cc];
    if (bcc !== undefined) payload.bcc = Array.isArray(bcc) ? bcc : [bcc];
    if (html !== undefined) payload.html = html;

    const result = await makeAgentMailRequest<any>(
      "POST",
      `/inboxes/${inbox_id}/messages/send`,
      apiKey,
      payload
    );

    if (!result) {
      return {
        content: [{ type: "text", text: "Failed to send message" }],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: `Message sent successfully. Message ID: ${
            result.message_id || "unknown"
          }`,
        },
      ],
    };
  }
);

// Add replyToMessage tool
server.tool(
  "replyToMessage",
  "Reply to an existing email message. Use this tool when the user asks to respond to an email, reply to someone, answer a message, or continue an email conversation.",
  {
    inbox_id: z.string().describe("ID of the inbox"),
    message_id: z.string().describe("ID of the message to reply to"),
    to: z
      .union([z.string(), z.array(z.string())])
      .optional()
      .describe("Recipient email address(es)"),
    cc: z
      .union([z.string(), z.array(z.string())])
      .optional()
      .describe("CC recipient(s)"),
    bcc: z
      .union([z.string(), z.array(z.string())])
      .optional()
      .describe("BCC recipient(s)"),
    text: z.string().optional().describe("Reply body content"),
    html: z.string().optional().describe("HTML reply body"),
    include_quoted_reply: z
      .boolean()
      .optional()
      .describe("Whether to include the original message as a quote"),
  },
  async ({
    inbox_id,
    message_id,
    to,
    cc,
    bcc,
    text,
    html,
    include_quoted_reply,
  }) => {
    const payload: Record<string, any> = {};

    if (to !== undefined) payload.to = Array.isArray(to) ? to : [to];
    if (cc !== undefined) payload.cc = Array.isArray(cc) ? cc : [cc];
    if (bcc !== undefined) payload.bcc = Array.isArray(bcc) ? bcc : [bcc];
    if (text !== undefined) payload.text = text;
    if (html !== undefined) payload.html = html;
    if (include_quoted_reply !== undefined)
      payload.include_quoted_reply = include_quoted_reply;

    const result = await makeAgentMailRequest<any>(
      "POST",
      `/inboxes/${inbox_id}/messages/${message_id}/reply`,
      apiKey,
      payload
    );

    if (!result) {
      return {
        content: [{ type: "text", text: "Failed to send reply" }],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: `Reply sent successfully. Message ID: ${
            result.message_id || "unknown"
          }`,
        },
      ],
    };
  }
);

// Add getAttachment tool
server.tool(
  "getAttachment",
  "Get details of a file attachment from an email. Use this tool when the user asks about email attachments, wants to access files sent in an email, or needs information about documents attached to messages.",
  {
    inbox_id: z.string().describe("ID of the inbox"),
    message_id: z.string().describe("ID of the message"),
    attachment_id: z.string().describe("ID of the attachment to retrieve"),
  },
  async ({ inbox_id, message_id, attachment_id }) => {
    const result = await makeAgentMailRequest<Attachment>(
      "GET",
      `/inboxes/${inbox_id}/messages/${message_id}/attachments/${attachment_id}`,
      apiKey
    );

    if (!result) {
      return {
        content: [
          {
            type: "text",
            text: `Failed to retrieve attachment with ID: ${attachment_id}`,
          },
        ],
      };
    }

    const attachmentText = `Attachment Details:
ID: ${result.attachment_id}
Filename: ${result.filename}
Content Type: ${result.content_type}
Size: ${result.size} bytes
URL: ${result.url}`;

    return {
      content: [{ type: "text", text: attachmentText }],
    };
  }
);

// Create a main function to handle async logic
async function main() {
  // Register server with transport
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Use console.error instead of console.log for logs
  console.error("AgentMail MCP server started. Waiting for requests...");
}

// Start the server
main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
