import pm4py
import re

log = pm4py.read_xes('logs/BPI_Challenge_2012.xes', return_legacy_log_object=True)
log_df  = pm4py.convert_to_dataframe(log)

unique = log_df["concept:name"].unique()
unique_O = list(filter(lambda n: re.match("O_.*", n), unique))

print("==================================================")
print("Unique_O: ", unique_O)
print("==================================================")

log_variants = pm4py.get_variants_as_tuples(log_df, activity_key='concept:name', timestamp_key='time:timestamp', case_id_key='case:concept:name')
print("Log events:   " , len(log_df))
print("Log cases:    " , len(log_df['case:concept:name'].unique()))
print("Log variants: ", len(log_variants))

O_filter_df = pm4py.filter_event_attribute_values(log_df, "concept:name", unique_O, "event", True, "case:concept:name")
O_df = pm4py.format_dataframe(O_filter_df, case_id='case:concept:name',activity_key='concept:name', timestamp_key='time:timestamp')
O_variants = pm4py.get_variants_as_tuples(O_df, activity_key='concept:name', timestamp_key='time:timestamp', case_id_key='case:concept:name')

print("O_ events: " , len(O_df))
print("O_ cases:  " , len(O_df['case:concept:name'].unique()))
print("O_ variants: ", len(O_variants))

index = 1
for O_variant,total in O_variants.items():
    print(O_variant, ", ", total)

    with open( "output/" + str(index) + ".txt", "w") as f:
        for event in O_variant:
            f.write(event + "\n")
    index = index + 1
