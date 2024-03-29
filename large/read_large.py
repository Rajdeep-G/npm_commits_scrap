   # {repo_name} {org_name}
with open('large_repo.txt', 'r') as file:
    lines = file.readlines()
    total_commits = 0
    for line in lines:
        try:
            repo_name, org_name, commit_count, _, _ = line.split()
        except ValueError:
            repo_name, org_name, commit_count, _ = line.split()

        with open('o_combined.txt', 'r') as out_f:
            lines_out = out_f.readlines()
            for line_out in lines_out:
                content=line_out.split()
                repo_name=repo_name.replace('_','/')
                org_name=org_name.replace('_','/')
                if repo_name==content[2] and org_name==content[0]:
                    with open('mod.txt', 'a') as f:
                        f.write(f'{content[0]} {content[1]} {content[2]} {content[3]}\n')
                    
                    

             