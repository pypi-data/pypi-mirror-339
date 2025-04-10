from pkg_resources import iter_entry_points

print("Registered source plugins:")
for ep in iter_entry_points("datahub.ingestion.source.plugins"):
    attr = f"{ep.module_name}:{ep.attrs[0]}" if ep.attrs else ep.module_name
    print(f"- {ep.name} -> {attr}")