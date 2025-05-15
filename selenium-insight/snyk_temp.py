import time

from selenium import webdriver
from selenium.webdriver.common.by import By

url_list = ['https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-MICROSOFTIDENTITYMODELJSONWEBTOKENS-6148656',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-MICROSOFTASPNETCORESERVERIIS-451561',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-SYSTEMIDENTITYMODELTOKENSJWT-6148655',
'https://app.snyk.io/org/pulse-boh/project/c1401078-a2ea-43d9-8ed1-d9ae626bf8af#issue-SNYK-DOTNET-MICROSOFTASPNETCORESERVERIIS-451561',
'https://app.snyk.io/org/pulse-boh/project/c1401078-a2ea-43d9-8ed1-d9ae626bf8af#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/c1401078-a2ea-43d9-8ed1-d9ae626bf8af#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/c1401078-a2ea-43d9-8ed1-d9ae626bf8af#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/c1401078-a2ea-43d9-8ed1-d9ae626bf8af#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/c1401078-a2ea-43d9-8ed1-d9ae626bf8af#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/dc104c1e-72a2-43e4-846e-93df8552718a#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/dc104c1e-72a2-43e4-846e-93df8552718a#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/dc104c1e-72a2-43e4-846e-93df8552718a#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/f4d3be3a-0c2c-4865-b2a8-6bf54f5d28fb#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/f4d3be3a-0c2c-4865-b2a8-6bf54f5d28fb#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/6ad12c19-c87b-43b8-bfb6-cfe291f34640#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/6ad12c19-c87b-43b8-bfb6-cfe291f34640#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/6ad12c19-c87b-43b8-bfb6-cfe291f34640#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/783270f1-b694-4254-8aa9-96455c35f7f5#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/f6a8e6e7-93ed-4cd8-a94e-ee24af19655e#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/8f472c02-1e06-4d45-82e5-c7237b61f3d3#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/8f472c02-1e06-4d45-82e5-c7237b61f3d3#issue-SNYK-JS-EXPRESS-6474509',
'https://app.snyk.io/org/pulse-boh/project/a3032065-9c07-4029-93f0-b7a0e8172985#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/276b2382-0f44-4ebe-b10d-0d0d67a30b2c#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/276b2382-0f44-4ebe-b10d-0d0d67a30b2c#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/276b2382-0f44-4ebe-b10d-0d0d67a30b2c#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/276b2382-0f44-4ebe-b10d-0d0d67a30b2c#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/276b2382-0f44-4ebe-b10d-0d0d67a30b2c#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/c90ef95b-31e3-4663-85bc-af2d94f58872#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/0640a4d5-f648-49fa-87a2-cfa62b190ffa#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/c90ef95b-31e3-4663-85bc-af2d94f58872#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/0640a4d5-f648-49fa-87a2-cfa62b190ffa#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/0640a4d5-f648-49fa-87a2-cfa62b190ffa#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/c90ef95b-31e3-4663-85bc-af2d94f58872#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/0640a4d5-f648-49fa-87a2-cfa62b190ffa#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/c90ef95b-31e3-4663-85bc-af2d94f58872#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/c90ef95b-31e3-4663-85bc-af2d94f58872#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/0640a4d5-f648-49fa-87a2-cfa62b190ffa#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/8b432d8c-8a3a-489d-b982-a68d85584ead#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/8b432d8c-8a3a-489d-b982-a68d85584ead#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/8b432d8c-8a3a-489d-b982-a68d85584ead#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/8b432d8c-8a3a-489d-b982-a68d85584ead#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/8b432d8c-8a3a-489d-b982-a68d85584ead#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-SYSTEMNETHTTP-60048',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/14a6d374-03a1-4ed4-a880-5660f8e07e10#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/14a6d374-03a1-4ed4-a880-5660f8e07e10#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/14a6d374-03a1-4ed4-a880-5660f8e07e10#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/14a6d374-03a1-4ed4-a880-5660f8e07e10#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/14a6d374-03a1-4ed4-a880-5660f8e07e10#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/dd67da45-92bd-4fad-973e-917dbc1db1e7#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/dd67da45-92bd-4fad-973e-917dbc1db1e7#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/dd67da45-92bd-4fad-973e-917dbc1db1e7#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/dd67da45-92bd-4fad-973e-917dbc1db1e7#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/dd67da45-92bd-4fad-973e-917dbc1db1e7#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/fc444aec-d186-4c54-a99a-903607a83348#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/fc444aec-d186-4c54-a99a-903607a83348#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/fc444aec-d186-4c54-a99a-903607a83348#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/fc444aec-d186-4c54-a99a-903607a83348#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/fc444aec-d186-4c54-a99a-903607a83348#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/03e77d0b-28bf-45a1-b4a7-c562082eaced#issue-SNYK-JS-JSON5-3182856',
'https://app.snyk.io/org/pulse-boh/project/03e77d0b-28bf-45a1-b4a7-c562082eaced#issue-SNYK-JS-RAMDA-1582370',
'https://app.snyk.io/org/pulse-boh/project/255ea1e5-e4a8-4bbc-b446-efeab96ab9d8#issue-SNYK-JS-INFLIGHT-6095116',
'https://app.snyk.io/org/pulse-boh/project/255ea1e5-e4a8-4bbc-b446-efeab96ab9d8#issue-SNYK-JS-MINIMATCH-3050818',
'https://app.snyk.io/org/pulse-boh/project/c314d2a6-3bb5-4021-85d1-fd970f0e1178#issue-SNYK-JS-ASYNC-7414156',
'https://app.snyk.io/org/pulse-boh/project/c314d2a6-3bb5-4021-85d1-fd970f0e1178#issue-SNYK-JS-INFLIGHT-6095116',
'https://app.snyk.io/org/pulse-boh/project/563e0cd0-cd61-4930-88a0-d167f20cfe84#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/563e0cd0-cd61-4930-88a0-d167f20cfe84#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/563e0cd0-cd61-4930-88a0-d167f20cfe84#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/c18088bc-1108-41f1-b2c6-0ae6e64b06d1#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/c18088bc-1108-41f1-b2c6-0ae6e64b06d1#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/c18088bc-1108-41f1-b2c6-0ae6e64b06d1#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/c18088bc-1108-41f1-b2c6-0ae6e64b06d1#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/c18088bc-1108-41f1-b2c6-0ae6e64b06d1#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/7cd329b7-ad46-4207-ae68-7eab699b6afd#issue-SNYK-DOTNET-MICROSOFTIDENTITYCLIENT-7246763',
'https://app.snyk.io/org/pulse-boh/project/7cd329b7-ad46-4207-ae68-7eab699b6afd#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONASPNETCORE-6613064',
'https://app.snyk.io/org/pulse-boh/project/7cd329b7-ad46-4207-ae68-7eab699b6afd#issue-SNYK-DOTNET-OPENTELEMETRYINSTRUMENTATIONHTTP-6613065',
'https://app.snyk.io/org/pulse-boh/project/7cd329b7-ad46-4207-ae68-7eab699b6afd#issue-SNYK-DOTNET-AZUREIDENTITY-6597976',
'https://app.snyk.io/org/pulse-boh/project/7cd329b7-ad46-4207-ae68-7eab699b6afd#issue-SNYK-DOTNET-AZUREIDENTITY-7246762',
'https://app.snyk.io/org/pulse-boh/project/537062db-57f6-48fe-883e-b0b5cd9596ce#issue-SNYK-JS-EXPRESS-6474509',
'https://app.snyk.io/org/pulse-boh/project/1462ffda-494d-40a7-8e6c-ca06a64b9163#issue-SNYK-JS-INFLIGHT-6095116',
'https://app.snyk.io/org/pulse-boh/project/1462ffda-494d-40a7-8e6c-ca06a64b9163#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/8f1e48ed-194e-4f84-96f0-5502723b6984#issue-SNYK-JS-INFLIGHT-6095116',
'https://app.snyk.io/org/pulse-boh/project/537062db-57f6-48fe-883e-b0b5cd9596ce#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/4885810e-2228-4022-98b2-df674974bdd9#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/7b15db01-c66a-4122-b8a1-c6c40263a26e#issue-SNYK-JS-GRPCGRPCJS-7242922',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-MICROSOFTDATASQLCLIENT-6149434',
'https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-AZUREIDENTITY-6009155',
'https://app.snyk.io/org/pulse-boh/project/783270f1-b694-4254-8aa9-96455c35f7f5#issue-SNYK-JS-IMPORTINTHEMIDDLE-5826054',
'https://app.snyk.io/org/pulse-boh/project/a3032065-9c07-4029-93f0-b7a0e8172985#issue-SNYK-JS-IMPORTINTHEMIDDLE-5826054',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-SYSTEMNETHTTP-60045',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-SYSTEMNETHTTP-60047',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-SYSTEMNETHTTP-72439',
'https://app.snyk.io/org/pulse-boh/project/39ed77dc-6ffc-4d7a-90a5-d0f8c01d8c6a#issue-SNYK-DOTNET-SYSTEMNETHTTP-60046',
'https://app.snyk.io/org/pulse-boh/project/7b15db01-c66a-4122-b8a1-c6c40263a26e#issue-SNYK-JS-IMPORTINTHEMIDDLE-5826054',
'https://app.snyk.io/org/pulse-boh/project/4885810e-2228-4022-98b2-df674974bdd9#issue-SNYK-JS-IMPORTINTHEMIDDLE-5826054',
]

driver = webdriver.Chrome()
driver.get('https://app.snyk.io/org/pulse-boh/project/de2bfe8c-87f2-4744-a152-130826573c5c#issue-SNYK-DOTNET-MICROSOFTIDENTITYMODELJSONWEBTOKENS-6148656')
time.sleep(50)

project_title_xpath = "//span[@class='project-details-title']/span[1]"
project_origin_name = "//span[@class='project-origin-name']"
introduced_through = "//div[contains(text(),'Introduced through')]/following-sibling::div"
content_frame = "//iframe[@data-testid]"

for snyk_url in url_list:
    driver.get(snyk_url)
    time.sleep(12.5)
    proj_title = driver.find_element(By.XPATH, project_title_xpath).text
    proj_origin = driver.find_element(By.XPATH, project_origin_name).text
    iframe = driver.find_element(By.XPATH, content_frame)
    driver.switch_to.frame(iframe)
    intro = driver.find_element(By.XPATH, introduced_through).text
    driver.switch_to.default_content()

    print(f"{snyk_url}\t{proj_origin}\t{intro}\t{proj_title}")

print("DONE")


