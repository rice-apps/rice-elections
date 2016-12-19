import { NgElectionsPage } from './app.po';

describe('ng-elections App', function() {
  let page: NgElectionsPage;

  beforeEach(() => {
    page = new NgElectionsPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
