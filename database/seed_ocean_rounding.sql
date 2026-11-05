INSERT INTO reservations (
    id, property_id, tenant_id, check_in_date, check_out_date, total_amount, currency
)
VALUES (
    'res-ocean-rounding-001',
    'prop-001',
    'tenant-b',
    '2024-03-15 15:00:00+00',
    '2024-03-16 15:00:00+00',
    10.075,
    'USD'
)
ON CONFLICT (id) DO UPDATE SET total_amount = EXCLUDED.total_amount;
