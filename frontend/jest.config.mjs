import nextJest from 'next/jest.js';

const createJestConfig = nextJest({ dir: './' });

/** @type {import('jest').Config} */
const config = {
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    testEnvironment: 'jest-environment-jsdom',

    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1',
    },

    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'mjs', 'json'],
};

export default createJestConfig(config);