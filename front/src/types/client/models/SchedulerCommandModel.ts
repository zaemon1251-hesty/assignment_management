/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Scheduler represents what assignment should be reminded to whom at a certain time
 */
export type SchedulerCommandModel = {
    submission_id?: number;
    remind_at?: string;
    reminded?: boolean;
};
