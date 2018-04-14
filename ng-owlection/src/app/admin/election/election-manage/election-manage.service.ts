import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of }         from 'rxjs/observable/of';
import 'rxjs/add/operator/delay';
import {InternalsElection} from "../../../internals/models/internals-election";



@Injectable()
export class ElectionManageService {

    delayMs = 500;

    getElections(): Observable<InternalsElection[]> {
        return of('/assets/internals-elections.json'["elections"]).delay(this.delayMs);
    }


    updateElections(election: InternalsElection): Observable<InternalsElection> {
        const oldElection = '/assets/internals-elections.json'["elections"].find(e => e.id === election.id);
        const newElection = Object.assign(oldElection, election);
        return of(newElection).delay(this.delayMs);
    }
}

