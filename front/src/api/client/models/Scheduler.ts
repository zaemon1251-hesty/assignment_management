/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Submission } from './Submission';

/**
 * Scheduler represents what assignment should be reminded to whom at a certain time
 */
export type Scheduler = {
    id?: number;
    submission_id: number;
    remind_at: string;
    reminded?: boolean;
    created_at?: string;
    updated_at?: string;
    submission?: Submission;
};
