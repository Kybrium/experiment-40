"use client";

import { useEffect } from "react";
import { APP_NAME, MODE, API_URL, modeColor } from "@/lib/tests/env";

function getBrowserDetails() {
    if (typeof window === "undefined") return null;

    const nav = navigator as any;
    const mem = (nav.deviceMemory ?? "n/a") + (nav.deviceMemory ? " GB" : "");
    const cores = nav.hardwareConcurrency ?? "n/a";
    const lang = navigator.language;
    const langs = navigator.languages?.join(", ") ?? lang;
    const online = navigator.onLine;
    const conn = (nav.connection?.effectiveType ?? "n/a") +
        (nav.connection?.downlink ? ` @ ${nav.connection.downlink}Mbps` : "");
    const ua = navigator.userAgent;
    const platform = navigator.platform;
    const cookieEnabled = navigator.cookieEnabled;
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;

    const screenInfo = `${window.screen.width}x${window.screen.height} (dpr ${window.devicePixelRatio || 1})`;
    const colorDepth = `${window.screen.colorDepth}-bit`;
    const url = window.location.href;
    const hostname = window.location.hostname;
    const viewport = `${Math.round(window.innerWidth)}x${Math.round(window.innerHeight)}`;

    return {
        app: APP_NAME,
        mode: MODE,
        api_url: API_URL,
        url,
        hostname,
        time: new Date().toISOString(),
        timezone: tz,
        language: lang,
        languages: langs,
        online,
        connection: conn,
        user_agent: ua,
        platform,
        device_memory: mem,
        cpu_cores: cores,
        screen: screenInfo,
        viewport,
        color_depth: colorDepth,
        cookie_enabled: cookieEnabled,
    };
}

export default function ConsoleStartup() {

    useEffect(() => {

        if (MODE === "PRODUCTION") return;

        const info = getBrowserDetails();
        if (!info) return;

        // Pretty banner
        const color = modeColor(MODE);
        const pad = "padding:6px 10px;";
        const base = "background:#0b0e14;color:#fff;" + pad;
        const left = `background:#0b0e14;color:#7dd3fc;border-radius:6px 0 0 6px;${pad}font-weight:700`;
        const mid = `background:#0b0e14;color:${color};${pad}`;
        const right = `background:#0b0e14;color:#9ca3af;border-radius:0 6px 6px 0;${pad}`;

        // eslint-disable-next-line no-console
        console.log(
            `%c ${APP_NAME} %c %c Mode: ${MODE} %c | API: ${API_URL}`,
            left, base, mid, right
        );

        // Collapsed groups with a table of details
        // eslint-disable-next-line no-console
        console.groupCollapsed(`🔎 Details (${APP_NAME})`);
        // eslint-disable-next-line no-console
        console.table(info);

        // Helpful sub-sections
        // eslint-disable-next-line no-console
        console.groupCollapsed("🌐 Location");
        // eslint-disable-next-line no-console
        console.log(`URL: ${info.url}`);
        // eslint-disable-next-line no-console
        console.log(`Hostname: ${info.hostname}`);
        // eslint-disable-next-line no-console
        console.log(`Timezone: ${info.timezone}`);
        // eslint-disable-next-line no-console
        console.groupEnd();

        // eslint-disable-next-line no-console
        console.groupCollapsed("💻 Device");
        // eslint-disable-next-line no-console
        console.log(`Platform: ${info.platform}`);
        // eslint-disable-next-line no-console
        console.log(`Cores: ${info.cpu_cores} • Memory: ${info.device_memory}`);
        // eslint-disable-next-line no-console
        console.log(`Screen: ${info.screen} • Viewport: ${info.viewport}`);
        // eslint-disable-next-line no-console
        console.log(`Color depth: ${info.color_depth}`);
        // eslint-disable-next-line no-console
        console.groupEnd();

        // eslint-disable-next-line no-console
        console.groupCollapsed("📶 Network");
        // eslint-disable-next-line no-console
        console.log(`Online: ${info.online}`);
        // eslint-disable-next-line no-console
        console.log(`Connection: ${info.connection}`);
        // eslint-disable-next-line no-console
        console.groupEnd();

        // eslint-disable-next-line no-console
        console.groupCollapsed("🗣️ Locale");
        // eslint-disable-next-line no-console
        console.log(`Language: ${info.language}`);
        // eslint-disable-next-line no-console
        console.log(`Languages: ${info.languages}`);
        // eslint-disable-next-line no-console
        console.groupEnd();

        // eslint-disable-next-line no-console
        console.groupEnd();
    }, []);

    return null; // purely side-effect in console
}