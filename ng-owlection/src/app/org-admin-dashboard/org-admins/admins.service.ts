import { Injectable } from '@angular/core';

import { ADMINS } from './admins';

@Injectable()
export class AdminsService {
  getAdmins(): Promise<string[]> {
    return Promise.resolve(ADMINS);
  }
}
