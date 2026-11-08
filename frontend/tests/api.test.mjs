import test, { beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";

import {
  ApiError,
  getSections,
  getStudentEnrollments,
  createEnrollment,
  deleteEnrollment,
} from "../src/api.js";

let originalFetch;

beforeEach(() => {
  originalFetch = globalThis.fetch;
});

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function mockResponse(data, status = 200) {
  return new Response(
    data === null ? null : JSON.stringify(data),
    {
      status,
      headers: { "Content-Type": "application/json" },
    },
  );
}

// Test 1: GET danh sách lớp học thành công
test("getSections returns section list", async () => {
  const sections = [
    {
      id: "WEB-01",
      course_code: "INT2204",
      capacity: 30,
      enrolled_count: 20,
      remaining_slots: 10,
    },
  ];

  globalThis.fetch = async (url) => {
    assert.equal(url, "http://127.0.0.1:8000/sections");
    return mockResponse(sections);
  };

  assert.deepEqual(await getSections(), sections);
});

// Test 2: GET danh sách đăng ký của sinh viên
test("getStudentEnrollments returns student enrollments", async () => {
  const enrollments = [
    {
      student_id: "22000004",
      class_section_id: "WEB-01",
      registered_at: null,
    },
  ];

  globalThis.fetch = async (url) => {
    assert.equal(
      url,
      "http://127.0.0.1:8000/students/22000004/enrollments",
    );
    return mockResponse(enrollments);
  };

  assert.deepEqual(
    await getStudentEnrollments("22000004"),
    enrollments,
  );
});

// Test 3: POST đăng ký lớp thành công
test("createEnrollment sends correct payload", async () => {
  const payload = {
    student_id: "22000004",
    class_section_id: "WEB-01",
  };

  globalThis.fetch = async (url, options) => {
    assert.equal(url, "http://127.0.0.1:8000/enrollments");
    assert.equal(options.method, "POST");
    assert.equal(
      options.headers["Content-Type"],
      "application/json",
    );
    assert.deepEqual(JSON.parse(options.body), payload);

    return mockResponse(payload, 201);
  };

  assert.deepEqual(await createEnrollment(payload), payload);
});

// Test 4: POST bị từ chối vì lớp đã đầy hoặc trùng đăng ký
test("createEnrollment handles HTTP 409", async () => {
  globalThis.fetch = async () =>
    mockResponse({ detail: "Section is full" }, 409);

  await assert.rejects(
    createEnrollment({
      student_id: "22000004",
      class_section_id: "WEB-01",
    }),
    (error) => {
      assert.ok(error instanceof ApiError);
      assert.equal(error.status, 409);
      assert.equal(error.message, "Section is full");
      return true;
    },
  );
});

// Test 5: POST bị từ chối vì sinh viên hoặc lớp không tồn tại
test("createEnrollment handles HTTP 404", async () => {
  globalThis.fetch = async () =>
    mockResponse({ detail: "Student not found" }, 404);

  await assert.rejects(
    createEnrollment({
      student_id: "22000004",
      class_section_id: "WEB-01",
    }),
    (error) => {
      assert.equal(error.status, 404);
      assert.equal(error.message, "Student not found");
      return true;
    },
  );
});

// Test 6: DELETE thành công với HTTP 204
test("deleteEnrollment handles HTTP 204 without parsing JSON", async () => {
  globalThis.fetch = async (url, options) => {
    assert.equal(
      url,
      "http://127.0.0.1:8000/enrollments/22000004/WEB-01",
    );
    assert.equal(options.method, "DELETE");

    return mockResponse(null, 204);
  };

  assert.equal(
    await deleteEnrollment("22000004", "WEB-01"),
    null,
  );
});

// Test 7: DELETE thất bại vì đăng ký không tồn tại
test("deleteEnrollment handles HTTP 404", async () => {
  globalThis.fetch = async () =>
    mockResponse({ detail: "Enrollment not found" }, 404);

  await assert.rejects(
    deleteEnrollment("22000004", "WEB-01"),
    (error) => {
      assert.equal(error.status, 404);
      assert.equal(error.message, "Enrollment not found");
      return true;
    },
  );
});

// Test 8: Không kết nối được backend
test("request handles network errors", async () => {
  globalThis.fetch = async () => {
    throw new Error("Connection refused");
  };

  await assert.rejects(
    getSections(),
    (error) => {
      assert.ok(error instanceof ApiError);
      assert.equal(error.status, 0);
      assert.match(error.message, /Không thể kết nối/);
      return true;
    },
  );
});
