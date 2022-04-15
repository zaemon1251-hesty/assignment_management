/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ASSIGNMENT_STATE } from './ASSIGNMENT_STATE';
import type { Course } from './Course';

/**
 * assignment represents your collection of assignment as an entity.
 */
export type Assignment = {
    id?: number;
    title: string;
    url?: string;
    info?: string;
    state?: ASSIGNMENT_STATE;
    course_id: number;
    end_at?: string;
    created_at?: string;
    updated_at?: string;
    course?: Course;
};
