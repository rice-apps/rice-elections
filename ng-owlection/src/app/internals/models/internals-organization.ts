import {Organization} from '../../shared/models/organization';

export class InternalsOrganization extends Organization {
  electionCount: number;
  voteCount: number;
  adminCount: number;
}
