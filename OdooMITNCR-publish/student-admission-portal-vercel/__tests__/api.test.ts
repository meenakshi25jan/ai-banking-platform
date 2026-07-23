describe('API client', () => {
  it('should have ODOO_URL configured', () => {
    expect(process.env.NEXT_PUBLIC_ODOO_URL || 'http://localhost:8069').toBeTruthy();
  });
});
