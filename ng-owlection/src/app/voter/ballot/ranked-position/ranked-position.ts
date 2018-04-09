export class RankedPosition {
  positionName: string;
  description: string;
  candidates: Candidate[];
  writeInAllowed: boolean;
  numOptions: number
}

export class Candidate {
  id: number;
  name: string;
  rank: number;
  writeIn?: boolean
}
