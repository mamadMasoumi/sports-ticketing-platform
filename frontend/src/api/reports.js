import apiClient from "./client";

export const submitReport = (payload) =>
  apiClient.post("/api/reports/submit/", payload).then((res) => res.data);

export const getMyReports = () =>
  apiClient.get("/api/reports/mine/").then((res) => res.data);

export const getAllReports = (statusFilter = "") => {
  const params = statusFilter ? { status_filter: statusFilter } : {};
  return apiClient.get("/api/reports/all/", { params }).then((res) => res.data);
};

export const reviewReport = (reportId) =>
  apiClient.post(`/api/reports/${reportId}/review/`).then((res) => res.data);
