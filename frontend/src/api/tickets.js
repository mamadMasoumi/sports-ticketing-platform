import apiClient from "./client";

export const searchTickets = (filters = {}) => {
  const params = {};

  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      params[key] = value;
    }
  });

  return apiClient
    .get("/api/tickets/search/", { params })
    .then((res) => res.data);
};

export const getTicketDetail = (ticketId) =>
  apiClient.get(`/api/tickets/${ticketId}/`).then((res) => res.data);
