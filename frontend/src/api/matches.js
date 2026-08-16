import apiClient from "./client";

export const getMatches = () =>
  apiClient.get("/api/matches/").then((res) => res.data);

export const reserveTicket = (ticketId) =>
  apiClient
    .post("/api/matches/reserve/", { ticket_id: ticketId })
    .then((res) => res.data);

export const cancelReservation = (reservationId) =>
  apiClient
    .post("/api/matches/cancel/", { reservation_id: reservationId })
    .then((res) => res.data);

export const getMyBookings = (statusFilter = "") => {
  const params = statusFilter ? { status_filter: statusFilter } : {};
  return apiClient
    .get("/api/matches/bookings/", { params })
    .then((res) => res.data);
};
