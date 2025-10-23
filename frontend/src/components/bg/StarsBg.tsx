"use client";

import { memo, useEffect, useMemo, useState } from "react";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import type { ISourceOptions } from "@tsparticles/engine";
import { InteractivityDetect } from "@tsparticles/engine";
import { loadSlim } from "@tsparticles/slim";


/**
 * Minecraft-like starfield:
 * - Square "pixel" stars
 * - Very gentle drift & twinkle
 * - Subtle interactions:
 *    - Hover: attract (soft pull)
 *    - Click: bubble (brief brighten/enlarge)
 * - Full-screen, fixed background
 * - Two layers for depth
 */
const StarsBg = () => {
    const [ready, setReady] = useState(false);

    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadSlim(engine);
        }).then(() => setReady(true));
    }, []);

    // Shared star style
    const baseStar = {
        shape: { type: "square" as const },
        size: { value: { min: 1, max: 2 } },
        color: { value: "#ffffff" },
        opacity: {
            value: { min: 0.55, max: 0.9 },
            animation: { enable: true, speed: 1.52, minimumValue: 0.4, sync: false },
        },
    };

    // Interactivity config (used by both layers)
    const interactivity = {
        detectsOn: InteractivityDetect.window,
        events: {
            onHover: { enable: true, mode: "attract" },
            onClick: { enable: true, mode: "bubble" },
        },
        modes: {
            attract: {
                distance: 90,
                duration: 0.3,
                speed: 0.1,
            },
            bubble: {
                distance: 140,
                duration: 0.4,
                size: 3,
                opacity: 1,
            },
        },
    } as const;

    // BACK layer (farther: dimmer, slower)
    const optionsBack = useMemo<ISourceOptions>(
        () => ({
            fpsLimit: 60,
            interactivity,
            detectRetina: true,
            background: { color: { value: "transparent" } },
            particles: {
                number: { value: 160, density: { enable: true, area: 1200 } },
                ...baseStar,
                opacity: {
                    ...baseStar.opacity,
                    value: { min: 0.4, max: 0.7 },
                    animation: { enable: true, speed: 0.16, minimumValue: 0.35, sync: false },
                },
                move: {
                    enable: true,
                    speed: 0.03,
                    random: true,
                    direction: "none",
                    straight: false,
                    outModes: { default: "out" },
                    drift: 0.02,
                },
                links: { enable: false },
            },
        }),
        []
    );

    // FRONT layer (nearer: a bit brighter/bigger, still subtle)
    const optionsFront = useMemo<ISourceOptions>(
        () => ({
            fpsLimit: 60,
            interactivity,
            detectRetina: true,
            background: { color: { value: "transparent" } },
            particles: {
                number: { value: 110, density: { enable: true, area: 1000 } },
                ...baseStar,
                size: { value: { min: 1, max: 2.2 } },
                opacity: {
                    ...baseStar.opacity,
                    value: { min: 0.6, max: 0.95 },
                    animation: { enable: true, speed: 0.2, minimumValue: 0.45, sync: false },
                },
                move: {
                    enable: true,
                    speed: 0.05,
                    random: true,
                    direction: "none",
                    straight: false,
                    outModes: { default: "out" },
                    drift: 0.03,
                },
                links: { enable: false },
            },
        }),
        []
    );

    if (!ready) return null;

    return (
        <div className="fixed inset-0 -z-10">
            {/* BG Color */}
            <div aria-hidden className="absolute inset-0 bg-background" />
            {/* Far stars */}
            <Particles id="mc-stars-back" options={optionsBack} className="absolute inset-0" />
            {/* Near stars */}
            <Particles id="mc-stars-front" options={optionsFront} className="absolute inset-0" />
        </div>
    );
}

export default memo(StarsBg);