-- 3PL Performance Analysis
-- Public BigQuery demonstration
--
-- The full source-to-fact transformation pipeline is intentionally private.
-- This file demonstrates the main analytical queries once a validated
-- fact_3pl_orders table has been created.

-- ============================================================
-- Q3: 3PL ONTIME PERFORMANCE
-- ============================================================

SELECT
  `3pl_name`,

  ROUND(
    SAFE_DIVIDE(
      COUNTIF(check_pickup_ontime = 'Ontime'),
      COUNTIF(check_pickup_ontime IS NOT NULL)
    ) * 100,
    2
  ) AS pickup_ontime_rate_pct,

  ROUND(
    SAFE_DIVIDE(
      COUNTIF(check_delivery_ontime = 'Ontime'),
      COUNTIF(check_delivery_ontime IS NOT NULL)
    ) * 100,
    2
  ) AS delivery_ontime_rate_pct,

  ROUND(
    SAFE_DIVIDE(
      COUNTIF(check_return_ontime = 'Ontime'),
      COUNTIF(check_return_ontime IS NOT NULL)
    ) * 100,
    2
  ) AS return_ontime_rate_pct

FROM `project.dataset.fact_3pl_orders`

GROUP BY `3pl_name`
ORDER BY `3pl_name`;


-- ============================================================
-- Q4A: COST + SPEED BY ROUTE x 3PL
-- ============================================================

SELECT
  route,
  `3pl_name`,
  ROUND(AVG(leadtime_delivery), 2) AS avg_delivery_leadtime_hours,
  ROUND(AVG(estimated_shipping_fee), 2) AS avg_estimated_shipping_fee

FROM `project.dataset.fact_3pl_orders`

WHERE route IN (
  'Cross region',
  'Intra city',
  'Special same region'
)

GROUP BY route, `3pl_name`
ORDER BY route, `3pl_name`;


-- ============================================================
-- Q4B: LATE DELIVERY RATE BY ROUTE x 3PL
-- ============================================================

SELECT
  route,
  `3pl_name`,

  COUNTIF(check_delivery_ontime IS NOT NULL)
    AS eligible_delivery_orders,

  COUNTIF(check_delivery_ontime = 'Late')
    AS late_delivery_orders,

  ROUND(
    SAFE_DIVIDE(
      COUNTIF(check_delivery_ontime = 'Late'),
      COUNTIF(check_delivery_ontime IS NOT NULL)
    ) * 100,
    2
  ) AS late_delivery_rate_pct

FROM `project.dataset.fact_3pl_orders`

WHERE route IN (
  'Cross region',
  'Intra city',
  'Special same region'
)

GROUP BY route, `3pl_name`
ORDER BY route, `3pl_name`;
