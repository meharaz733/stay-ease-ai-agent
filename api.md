# StayEase API Contract

Base URL: `https://api.stayease.com`  
Content-Type: `application/json`  
---

## POST `/api/chat/{conversation_id}/message`

Send a guest message to the AI booking agent.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `conversation_id` | `string (UUID)` | Unique session identifier. Create a new UUID for a new guest session. |

### Request Body

```json
{
  "message": "string",
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | `string` | ✅ | The guest's message text |

### Response Body — `200 OK`

```json
{
  "conversation_id": "string (UUID)",
  "reply": "string",
  "timestamp": "string (ISO 8601)"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `conversation_id` | `string` | Echoed conversation ID |
| `reply` | `string` | Agent's response to the guest |
| `timestamp` | `string` | UTC timestamp of the response |

---

### Example — Property Search

**Request:**
```http
POST /api/chat/a1b2c3d4-e5f6-7890-abcd-ef1234567890/message
Content-Type: application/json

{
  "message": "আমি Cox's Bazar-এ ২ মে থেকে ৪ মে পর্যন্ত ২ জনের জন্য একটা রুম খুঁজছি।",
}
```

**Response `200 OK`:**
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "reply": "কক্সবাজারে ২ মে–৪ মে (২ রাত) ২ জনের জন্য আমি ২টি প্রপার্টি পেয়েছি:\n\n1. 🏨 Sea Pearl Beach Resort — ৳4,500/রাত (মোট ৳9,000)\n   সমুদ্রের পাড়ে রুম, AC, ফ্রি WiFi, বালকনি সহ। রেটিং: ⭐ 4.7\n\n2. 🏡 Coral View Guesthouse — ৳2,800/রাত (মোট ৳5,600)\n   বাজেট-ফ্রেন্ডলি, বিচ থেকে ৫ মিনিটের হাঁটা পথ। রেটিং: ⭐ 4.2\n\nকোনটা সম্পর্কে আরও জানতে চান?",
  "timestamp": "2026-05-01T10:23:45Z"
}
```

---

### Example — Booking Confirmation

**Request:**
```http
POST /api/chat/a1b2c3d4-e5f6-7890-abcd-ef1234567890/message
Content-Type: application/json

{
  "message": "Sea Pearl Beach Resort বুক করতে চাই। আমার নাম Rahim Uddin।",
}
```

**Response `200 OK`:**
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "reply": "✅ বুকিং কনফার্ম হয়েছে! আপনার বুকিং রেফারেন্স: BKG-20260501-042\n\n📋 বিবরণ:\n- প্রপার্টি: Sea Pearl Beach Resort, কক্সবাজার\n- চেক-ইন: ২ মে ২০২৬\n- চেক-আউট: ৪ মে ২০২৬\n- মোট মূল্য: ৳9,000\n\nধন্যবাদ StayEase বেছে নেওয়ার জন্য! 🙏",
  "timestamp": "2026-05-01T10:31:12Z"
}
```

---

### Example — Human Escalation

**Request:**
```http
POST /api/chat/a1b2c3d4-e5f6-7890-abcd-ef1234567890/message
Content-Type: application/json

{
  "message": "আমার বুকিং পেমেন্টে সমস্যা হচ্ছে, রিফান্ড চাই।",
}
```

**Response `200 OK`:**
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "reply": "দুঃখিত, আমি শুধু প্রপার্টি সার্চ, তথ্য এবং বুকিং করতে পারি। আপনার রিফান্ড সংক্রান্ত বিষয়ে আমাদের একজন টিম মেম্বার শীঘ্রই যোগাযোগ করবেন। 🙏",
  "timestamp": "2026-05-01T10:35:00Z"
}
```

---

### Error Responses

| Status | Code | Description |
|--------|------|-------------|
| `400` | `INVALID_REQUEST` | Missing required fields or malformed JSON |
| `404` | `CONVERSATION_NOT_FOUND` | `conversation_id` does not exist |
| `422` | `VALIDATION_ERROR` | Field type or constraint violation |
| `429` | `RATE_LIMITED` | Too many requests — max 30/min per conversation |
| `500` | `INTERNAL_ERROR` | Unexpected server or LLM error |
| `503` | `LLM_UNAVAILABLE` | Groq API temporarily unreachable |

**Error response format:**
```json
{
  "error": {
    "code": "400",
    "message": "Field 'message' is required.",
    "timestamp": "2026-05-01T10:23:45Z"
  }
}
```

---

## GET `/api/chat/{conversation_id}/history`

Retrieve the full message history for a conversation session.

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `conversation_id` | `string (UUID)` | Conversation session to retrieve |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | `integer` | `50` | Max messages to return (max 200) |
| `offset` | `integer` | `0` | Pagination offset |

### Response Body — `200 OK`

```json
{
  "conversation_id": "string (UUID)",
  "guest_phone": "string",
  "guest_email": "string | null",
  "messages": [
    {
      "role": "user | assistant",
      "message": "string",
      "timestamp": "string (ISO 8601)"
    }
  ],
  "total_messages": "integer",
  "is_human_needed": "boolean",
  "human_handover_reason": "string | null",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

---

### Example

**Request:**
```http
GET /api/chat/a1b2c3d4-e5f6-7890-abcd-ef1234567890/history?limit=10
```

**Response `200 OK`:**
```json
{
  "conversation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "guest_phone": "01700000000",
  "guest_email": "guest@gmail.com",
  "messages": [
    {
      "role": "user",
      "message": "আমি Cox's Bazar-এ ২ মে থেকে ৪ মে পর্যন্ত ২ জনের জন্য একটা রুম খুঁজছি।",
      "timestamp": "2026-05-01T10:23:40Z"
    },
    {
      "role": "assistant",
      "message": "কক্সবাজারে ২ মে–৪ মে (২ রাত) ২ জনের জন্য আমি ২টি প্রপার্টি পেয়েছি:\n\n1. 🏨 Sea Pearl Beach Resort — ৳4,500/রাত...",
      "timestamp": "2026-05-01T10:23:45Z"
    },
    {
      "role": "user",
      "message": "Sea Pearl Beach Resort বুক করতে চাই। আমার নাম Rahim Uddin।",
      "timestamp": "2026-05-01T10:31:08Z"
    },
    {
      "role": "assistant",
      "message": "✅ বুকিং কনফার্ম হয়েছে! আপনার বুকিং রেফারেন্স: BKG-20260501-042...",
      "timestamp": "2026-05-01T10:31:12Z"
    }
  ],
  "total_messages": 4,
  "is_needs_human": false,
  "human_handover_reason": null,
  "created_at": "2026-05-01T10:23:40Z",
  "updated_at": "2026-05-01T10:31:12Z"
}
```

---

### Error Responses

| Status | Code | Description |
|--------|------|-------------|
| `400` | `INVALID_REQUEST` | Missing required fields or malformed JSON |
| `404` | `CONVERSATION_NOT_FOUND` | No conversation with this ID exists |
| `422` | `VALIDATION_ERROR` | Invalid `limit` or `offset` values |
| `500` | `INTERNAL_ERROR` | Unexpected server error |
