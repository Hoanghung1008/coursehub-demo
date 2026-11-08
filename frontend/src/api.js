const BASE_URL = (
  import.meta.env?.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

export class ApiError extends Error {
  constructor(message, status = 0, details = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

export async function api(path, {
  method = "GET",
  body,
  signal,
  headers: customHeaders = {},
} = {}) {
  const headers = {
    Accept: "application/json",
    ...(body !== undefined
      ? { "Content-Type": "application/json" }
      : {}),
    ...customHeaders,
  };

  let response;

  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      signal,
      ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw error;
    }

    throw new ApiError(
      "Không thể kết nối đến máy chủ. Vui lòng kiểm tra backend.",
      0,
      error.message,
    );
  }

  if (response.status === 204) {
    return null;
  }

  let data = null;

  try {
    const raw = await response.text();
    data = raw ? JSON.parse(raw) : null;
  } catch {
    if (response.ok) {
      throw new ApiError(
        `HTTP ${response.status}: phản hồi không phải JSON.`,
        response.status,
      );
    }
  }

  if (!response.ok) {
    const detail = data?.detail;

    const message = typeof detail === "string"
      ? detail
      : Array.isArray(detail)
        ? detail.map((item) => item.msg).join("; ")
        : `Yêu cầu thất bại (HTTP ${response.status})`;

    throw new ApiError(message, response.status, data);
  }

  return data;
}

export function getCourses(options) {
  return api("/courses", options);
}

export function getSections(options) {
  return api("/sections", options);
}

export function getStudentEnrollments(studentId, options) {
  return api(
    `/students/${encodeURIComponent(studentId)}/enrollments`,
    options,
  );
}

export function createEnrollment(data) {
  return api("/enrollments", {
    method: "POST",
    body: data,
  });
}

export function deleteEnrollment(studentId, sectionId) {
  return api(
    `/enrollments/${encodeURIComponent(studentId)}/${encodeURIComponent(sectionId)}`,
    { method: "DELETE" },
  );
}
