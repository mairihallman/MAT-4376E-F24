# Mairi's (very messy) notes
[FiveThirtyEight polling average methodology](https://fivethirtyeight.com/methodology/how-our-polling-averages-work/) - guideline for us?

- polls of likely voters > polls of registered voters > polls of all adults
- cap sample sizes at 5000, windsorize (idk if windsorizing makes sense here)
- if sample size isn't reported, use median sample size of polls from that polster of that type (if no other info, use median sample size of all other polls of that type) - note type doesn't matter for us
- for overlapping polls from a given firm -  dynamically remove polls with overlapping dates until greatest number of polls with no overlapping dates is retained (no)
- sample size weighting - square root of poll's sample size / square root for median sample size for group

[Pollster Rating Calculation](https://fivethirtyeight.com/features/how-fivethirtyeight-calculates-pollster-ratings/)
- grade corresponds to predictive plus-minus

# Ideas
- augment dataset with electoral college points?
- [how electoral college works](https://chatgpt.com/share/66e84bb5-ca58-8006-99ad-7697cf58228d)

# 1 Oct - Draft Report

## Introduction
Hillary Clinton's loss to Donald Trump in the 2016 American presidential election was as unexpected as it was humiliating. How did a former senator, first lady, and secretary of state lose to a washed-up reality TV star who, just a month before the election, made headlines for a resurfaced video in which he bragged about sexual assault?

Clinton has attributed much of the blame for her defeat to former FBI Director James Comey. On October 28, 2016, Comey sent a letter to Congress outlining the FBI's decision to reopen an investigation into Clinton's use of a private email server. The ensuing media circus dominated the news cycle during the final stretch of the campaign. Two days before the election, on November 6th, Comey announced that the new evidence did not warrant reopening the investigation after all.

Given how things turned out, it's understandable that Clinton feels Comey "shivved" her. This investigation will explore whether there is evidence to support that claim. It will also provide a comprehensive overview of polling methodology and the American electoral system. Readers are invited to consider ethical questions about the role of government officials and the media in ensuring free and fair elections.

## Graph

Below is an exploration of aggregated raw polling data, as well as a moving average, for national polls and several swing states. These states had the tightest margins in the country, and Trump won them all. It is also worth noting that all of these states voted for Barack Obama in 2012 and Joe Biden in 2016. A noticeable drop in the polls' moving average after October 31st is oservable for all of the listed states except for Wisconsin, as well as the national polls.

Here, we have a direct comparison of the weighted average polls from Florida, Michigan, and Pensylvania. In all cases, there is a noticeable increase after the first presidential debate, and a decrease after Comey's letter. In terms of electoral college votes, Florida alone would've been sufficient for Clinton to win.




