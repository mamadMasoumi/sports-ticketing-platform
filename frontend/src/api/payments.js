import apiClient from "./client";

export const payForReservation = (reservationId, method) =>
  apiClient
    .post("/api/payments/pay/", { reservation_id: reservationId, method })
    .then((res) => res.data);
