describe('UI Tests', () => {
    it('should load the home page', () => {
        cy.visit('/');
        cy.contains('SASDS'); // Replace with actual content on your page
    });
});
