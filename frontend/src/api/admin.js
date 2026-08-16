import apiClient from "./client";

export const adminCancelReservation = (reservationId) =>
  apiClient
    .post(`/api/matches/${reservationId}/admin-cancel/`)
    .then((res) => res.data);
