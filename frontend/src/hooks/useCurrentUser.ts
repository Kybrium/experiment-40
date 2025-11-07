"use client";

import { fetchCurrentUser } from "@/endpoints/auth";
import { useQuery, useQueryClient } from "@tanstack/react-query";

interface UseCurrentUserOptions {
    /** If true, do not triggers the API fetch — only uses cache. */
    skip?: boolean;
}

export function useCurrentUser(options: UseCurrentUserOptions = {}) {
    const { skip = false } = options;
    const queryClient = useQueryClient();

    const query = useQuery({
        queryKey: ["me"],
        queryFn: fetchCurrentUser,
        staleTime: 5 * 60 * 1000,
        enabled: !skip,
    });

    const clearUser = () => {
        queryClient.setQueryData(["me"], null);
    };

    const hasCachedUser = () => {
        const cached = queryClient.getQueryData(["me"]);
        return Boolean(cached);
    };

    return { ...query, clearUser, hasCachedUser };
}