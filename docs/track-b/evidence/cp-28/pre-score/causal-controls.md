# CP-28 causal controls — protocol §10, proved before any run on stored forecasts

Run: `python -m pytest -v tests/cp28` (log: `causal-controls-tests.log`, 38 passed), on synthetic
ledgers only. The production replay is the same `cp28.engine.run` with 364/728/28. The scorer was
checked separately against CP-26's stored v5 and B0 losses (`scoring-validation.json`: 2,068 dates
each, maximum relative difference 3.4e-16). No CP-28 arm existed when either ran.

| §10 control | Negative / positive | Test (`tests/cp28/…`) |
|---|---|---|
| Target-day masking produces zero change | negative; D+2 release changes it (positive) | `test_cp28_causal_controls.py::test_target_day_masking_produces_zero_change_and_a_released_change_follows`, `::test_truth_is_never_requested_beyond_d_minus_2` |
| Available past-input mutation produces an appropriate change | positive | `::test_available_past_input_mutation_changes_the_forecast` |
| D−1 error mutation produces zero change | negative | `::test_d_minus_1_error_mutation_produces_zero_change`; the price predictor's use of D−1 (positive) and refusal of D (negative): `::test_d_minus_1_price_is_a_predictor_not_feedback` |
| D−2 released error can change learning | positive | `::test_d_minus_2_released_error_can_change_learning` |
| Duplicate release changes no buffer | negative | `::test_duplicate_release_changes_no_buffer` |
| Future rows change no training/scaler feature | negative | `::test_future_rows_change_no_training_or_scaler_feature` |
| Permuted outcomes cannot move calendar masks | negative; the losses do move (positive) | `test_cp28_pipeline.py::test_permuted_outcomes_cannot_move_calendar_masks` (every arm's paired dates and all twenty cells identical under permuted outcomes); the frozen keys come from CP-25 through the ledger |
| Copied fallback errors cannot enter member or arm H history | negative; neighbouring native dates enter (positive) | `::test_copied_fallback_errors_never_enter_member_or_arm_history` |
| Valid native centrals on H-history fallback dates enter after D−2, once | positive | `::test_valid_native_central_on_h_shortage_dates_enters_once_after_d_minus_2` |
| Hard central failures never enter | negative; the unaffected network arms enter (positive) | `::test_hard_central_failures_never_enter` (missing scale; injected solver failure → A2's complete forecast) |
| DST canonical keys survive | — | `::test_dst_canonical_keys_survive` (25-hour 2020-10-25 with both 02:00 hours in night; 23-hour 2020-03-29) |
| A3/A6 and A5/A7 share the identical unshrunk fits | — | `::test_shared_unshrunk_fits_and_deployment_rules`, `::test_startup_learned_arm_is_native_not_a_fallback` |
| Grid tie order | — | `test_cp28_units.py::test_grid_enumeration_order_and_size`, `::test_grid_tie_breaks_by_integer_distance_then_lowest_index` |
| Adam/L2 gradient | — | `::test_gradient_matches_finite_differences_including_the_l2_term`, `::test_adam_update_rule_and_deterministic_fit`, `::test_seed_and_initialization_are_the_registered_draws`, `::test_scaler_uses_row_weights_and_zero_sd_scale_one` |
| Actual-hour day weighting | — | `::test_each_date_weighs_equally_including_dst_lengths`, `::test_meta_loss_is_mean_daily_mae`, `::test_weighted_central_uses_the_grid_arithmetic` |
| One-sided null boundary | negative; a clear improvement rejects (positive) | `::test_one_sided_boundary_and_degenerate_endpoints` |
| Twenty-endpoint maximum | — | `::test_twenty_endpoints_and_the_compound_maximum` (a deficient cell sets p = 1) |
| Holm | — | `::test_holm_step_down_and_adjusted_p` |
| Every sensitivity rule | — | `::test_sensitivity_variants_and_pass_rule`, `::test_runs_split_at_gaps_and_years_and_join_2020_to_2021`, `::test_draw_plan_and_hac_match_cp26_reference` |
| Scores and selection | — | `::test_wis_matches_the_registered_formula`, `::test_selection_ties_and_simplicity_order`, `test_cp28_pipeline.py` |
