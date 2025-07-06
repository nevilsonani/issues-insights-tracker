export type Role = 'ADMIN' | 'MAINTAINER' | 'REPORTER';

export interface User {
  id: number;
  email: string;
  full_name?: string;
  role: Role;
}

export type Severity = 'LOW' | 'MEDIUM' | 'HIGH';
export type Status = 'OPEN' | 'TRIAGED' | 'IN_PROGRESS' | 'DONE';
export type Priority = 'BLOCKER' | 'CRITICAL' | 'MINOR' | 'TRIVIAL';

export interface Issue {
  id: number;
  title: string;
  description: string;
  severity: Severity;
  status: Status;
  priority?: Priority;
  file_path?: string;
  reporter_id: number;
  created_at: string;
  tags: string[];
}

export interface IssueCreate {
  title: string;
  description: string;
  severity: Severity;
  priority?: Priority;
}

export interface IssueUpdate {
  status: Status;
  priority?: Priority;
}

export interface UserCreate {
  email: string;
  full_name?: string;
  password: string;
  role?: Role;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface DailyStats {
  date: string;
  status: string;
  count: number;
}

export interface AnalyticsStats {
  total_issues: number;
  open_issues: number;
  in_progress_issues: number;
  completed_issues: number;
  high_priority_issues: number;
  medium_priority_issues: number;
  low_priority_issues: number;
  recent_issues: Issue[];
  issues_by_status: Record<string, number>;
  issues_by_severity: Record<string, number>;
}
