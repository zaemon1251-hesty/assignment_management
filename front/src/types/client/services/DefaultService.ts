/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Assignment } from '../models/Assignment';
import type { AssignmentCommandModel } from '../models/AssignmentCommandModel';
import type { AuthedUser } from '../models/AuthedUser';
import type { Body_create_token_api_users_login_post } from '../models/Body_create_token_api_users_login_post';
import type { Course } from '../models/Course';
import type { CourseCommandModel } from '../models/CourseCommandModel';
import type { Scheduler } from '../models/Scheduler';
import type { SchedulerCommandModel } from '../models/SchedulerCommandModel';
import type { Submission } from '../models/Submission';
import type { SubmissionCommandModel } from '../models/SubmissionCommandModel';
import type { Token } from '../models/Token';
import type { User } from '../models/User';
import type { UserCommandModel } from '../models/UserCommandModel';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Get
     * @param assignmentId
     * @returns Assignment Successful Response
     * @throws ApiError
     */
    public static getApiAssignmentsAssignmentIdGet(
        assignmentId: number,
    ): CancelablePromise<Assignment> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/assignments/{assignment_id}',
            path: {
                'assignment_id': assignmentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete
     * @param assignmentId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteApiAssignmentsAssignmentIdDelete(
        assignmentId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/assignments/{assignment_id}',
            path: {
                'assignment_id': assignmentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get All
     * @param requestBody
     * @returns Assignment Successful Response
     * @throws ApiError
     */
    public static getAllApiAssignmentsGet(
        requestBody?: Assignment,
    ): CancelablePromise<Array<Assignment>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/assignments/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add
     * @param requestBody
     * @returns Assignment Successful Response
     * @throws ApiError
     */
    public static addApiAssignmentsAddPost(
        requestBody: Assignment,
    ): CancelablePromise<Assignment> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/assignments/add',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update
     * @param assingnmentId
     * @param requestBody
     * @returns Assignment Successful Response
     * @throws ApiError
     */
    public static updateApiAssignmentsAssingnmentIdPut(
        assingnmentId: number,
        requestBody: AssignmentCommandModel,
    ): CancelablePromise<Assignment> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/assignments/{assingnment_id}',
            path: {
                'assingnment_id': assingnmentId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change State
     * @param assignmentId
     * @param state
     * @returns Assignment Successful Response
     * @throws ApiError
     */
    public static changeStateApiAssignmentsChangeAssignmentIdStatePatch(
        assignmentId: number,
        state: number,
    ): CancelablePromise<Assignment> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/assignments/change/{assignment_id}/{state}',
            path: {
                'assignment_id': assignmentId,
                'state': state,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Check Expire
     * @returns any Successful Response
     * @throws ApiError
     */
    public static checkExpireApiAssignmentsCheckExpireGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/assignments/check_expire',
        });
    }

    /**
     * Get
     * @param userId
     * @returns User Successful Response
     * @throws ApiError
     */
    public static getApiUsersUserIdGet(
        userId: number,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update
     * @param userId
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static updateApiUsersUserIdPut(
        userId: number,
        requestBody: UserCommandModel,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete
     * @param userId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteApiUsersUserIdDelete(
        userId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Authorize User
     * @returns AuthedUser Successful Response
     * @throws ApiError
     */
    public static authorizeUserApiUsersAuthenticateGet(): CancelablePromise<AuthedUser> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/_authenticate',
        });
    }

    /**
     * Get All
     * @param name
     * @param disabled
     * @returns User Successful Response
     * @throws ApiError
     */
    public static getAllApiUsersGet(
        name?: string,
        disabled?: boolean,
    ): CancelablePromise<Array<User>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/',
            query: {
                'name': name,
                'disabled': disabled,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create
     * @param requestBody
     * @returns UserCommandModel Successful Response
     * @throws ApiError
     */
    public static createApiUsersAddPost(
        requestBody: UserCommandModel,
    ): CancelablePromise<UserCommandModel> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/add',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change Password
     * @param userId
     * @param password
     * @returns User Successful Response
     * @throws ApiError
     */
    public static changePasswordApiUsersChangePasswordUserIdPatch(
        userId: number,
        password: string,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/users/change_password/{user_id}',
            path: {
                'user_id': userId,
            },
            query: {
                'password': password,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Token
     * @param formData
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static createTokenApiUsersLoginPost(
        formData?: Body_create_token_api_users_login_post,
    ): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get
     * @param courseId
     * @returns Course Successful Response
     * @throws ApiError
     */
    public static getApiCoursesCourseIdGet(
        courseId: number,
    ): CancelablePromise<Course> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/courses/{course_id}',
            path: {
                'course_id': courseId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update
     * @param courseId
     * @param requestBody
     * @returns Course Successful Response
     * @throws ApiError
     */
    public static updateApiCoursesCourseIdPut(
        courseId: number,
        requestBody: CourseCommandModel,
    ): CancelablePromise<Course> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/courses/{course_id}',
            path: {
                'course_id': courseId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete
     * @param courseId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteApiCoursesCourseIdDelete(
        courseId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/courses/{course_id}',
            path: {
                'course_id': courseId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get All
     * @param requestBody
     * @returns Course Successful Response
     * @throws ApiError
     */
    public static getAllApiCoursesGet(
        requestBody?: Course,
    ): CancelablePromise<Array<Course>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/courses/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add
     * @param requestBody
     * @returns Course Successful Response
     * @throws ApiError
     */
    public static addApiCoursesAddPost(
        requestBody: Course,
    ): CancelablePromise<Course> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/courses/add',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Scraping
     * @returns any Successful Response
     * @throws ApiError
     */
    public static scrapingApiCoursesAutoScrapingPost(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/courses/auto_scraping',
        });
    }

    /**
     * Get
     * @param submissionId
     * @returns Submission Successful Response
     * @throws ApiError
     */
    public static getApiSubmissionsSubmissionIdGet(
        submissionId: number,
    ): CancelablePromise<Submission> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/submissions/{submission_id}',
            path: {
                'submission_id': submissionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update
     * @param submissionId
     * @param requestBody
     * @returns Submission Successful Response
     * @throws ApiError
     */
    public static updateApiSubmissionsSubmissionIdPut(
        submissionId: number,
        requestBody: SubmissionCommandModel,
    ): CancelablePromise<Submission> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/submissions/{submission_id}',
            path: {
                'submission_id': submissionId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete
     * @param submissionId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteApiSubmissionsSubmissionIdDelete(
        submissionId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/submissions/{submission_id}',
            path: {
                'submission_id': submissionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get All
     * @param userId
     * @param submissionState
     * @param assignmentState
     * @param assignmentEndAt
     * @param assignmentEndAf
     * @param assignmentEndBe
     * @returns Submission Successful Response
     * @throws ApiError
     */
    public static getAllApiSubmissionsGet(
        userId?: number,
        submissionState?: string,
        assignmentState?: string,
        assignmentEndAt?: string,
        assignmentEndAf?: string,
        assignmentEndBe?: string,
    ): CancelablePromise<Array<Submission>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/submissions/',
            query: {
                'user_id': userId,
                'submission_state': submissionState,
                'assignment_state': assignmentState,
                'assignment_end_at': assignmentEndAt,
                'assignment_end_af': assignmentEndAf,
                'assignment_end_be': assignmentEndBe,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add
     * @param requestBody
     * @returns Submission Successful Response
     * @throws ApiError
     */
    public static addApiSubmissionsAddPost(
        requestBody: Submission,
    ): CancelablePromise<Submission> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/submissions/add',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change State
     * @param submissionId
     * @param state
     * @returns Submission Successful Response
     * @throws ApiError
     */
    public static changeStateApiSubmissionsChangeSubmissionIdStatePatch(
        submissionId: number,
        state: number,
    ): CancelablePromise<Submission> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/submissions/change/{submission_id}/{state}',
            path: {
                'submission_id': submissionId,
                'state': state,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get
     * @param schedulerId
     * @returns Scheduler Successful Response
     * @throws ApiError
     */
    public static getApiSchedulersSchedulerIdGet(
        schedulerId: number,
    ): CancelablePromise<Scheduler> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/schedulers/{scheduler_id}',
            path: {
                'scheduler_id': schedulerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update
     * @param schedulerId
     * @param requestBody
     * @returns Scheduler Successful Response
     * @throws ApiError
     */
    public static updateApiSchedulersSchedulerIdPut(
        schedulerId: number,
        requestBody: SchedulerCommandModel,
    ): CancelablePromise<Scheduler> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/schedulers/{scheduler_id}',
            path: {
                'scheduler_id': schedulerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete
     * @param schedulerId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteApiSchedulersSchedulerIdDelete(
        schedulerId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/schedulers/{scheduler_id}',
            path: {
                'scheduler_id': schedulerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get All
     * @param submissionId
     * @param reminded
     * @param remindAt
     * @param remindAf
     * @param remindBe
     * @returns Scheduler Successful Response
     * @throws ApiError
     */
    public static getAllApiSchedulersGet(
        submissionId?: number,
        reminded?: boolean,
        remindAt?: string,
        remindAf?: string,
        remindBe?: string,
    ): CancelablePromise<Array<Scheduler>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/schedulers/',
            query: {
                'submission_id': submissionId,
                'reminded': reminded,
                'remind_at': remindAt,
                'remind_af': remindAf,
                'remind_be': remindBe,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add
     * @param requestBody
     * @returns Scheduler Successful Response
     * @throws ApiError
     */
    public static addApiSchedulersAddPost(
        requestBody: Scheduler,
    ): CancelablePromise<Scheduler> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/schedulers/add',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Deadline Reminder
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deadlineReminderApiSchedulersDeadlineReminderPost(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/schedulers/deadline_reminder',
        });
    }

    /**
     * Add Remind Schedule
     * @param by
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addRemindScheduleApiSchedulersAddRemindSchdulePost(
        by?: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/schedulers/add_remind_schdule',
            query: {
                'by': by,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Redirects
     * @returns void
     * @throws ApiError
     */
    public static redirectsApiGet(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/',
            errors: {
                302: `Successful Response`,
            },
        });
    }

    /**
     * Healthz
     * @returns any Successful Response
     * @throws ApiError
     */
    public static healthzGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }

}