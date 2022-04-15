/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Assignment } from './Assignment';
import type { SUBMISSION_STATE } from './SUBMISSION_STATE';

/**
 * submission represents your registerd assignment as an entity.
 */
export type Submission = {
    id?: number;
    user_id: number;
    assignment_id: number;
    state?: SUBMISSION_STATE;
    created_at?: string;
    updated_at?: string;
    assignment?: Assignment;
};
