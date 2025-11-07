'use client';

export type Mode = "DEV" | "TEST" | "STAGING" | "PRODUCTION";

export const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME ?? "Experiment 40";
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export const MODE: Mode =
    (process.env.NEXT_PUBLIC_MODE?.toUpperCase() as Mode) ||
    (process.env.NODE_ENV === "production" ? "PRODUCTION" : "DEV");

export function modeColor(mode: Mode) {
    switch (mode) {
        case "DEV": return "#22c55e";
        case "TEST": return "#f59e0b";
        case "STAGING": return "#06b6d4";
        case "PRODUCTION": return "#ef4444";
    }
}